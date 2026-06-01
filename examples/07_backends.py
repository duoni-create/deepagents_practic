from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic.tools05 import get_backend_plan, pretty_json


# 中文说明：内存后端示例，把文件内容保存在字典里，进程结束后不会持久化。
class StateBackend:
    # 中文说明：初始化内存文件表。
    def __init__(self) -> None:
        self.files: dict[str, str] = {}

    # 中文说明：把指定路径的内容写入内存字典。
    def write(self, path: str, content: str) -> None:
        self.files[path] = content

    # 中文说明：从内存字典读取指定路径的内容。
    def read(self, path: str) -> str:
        return self.files[path]


# 中文说明：本地文件后端示例，把文件内容真正写到临时目录中。
class FilesystemBackend:
    # 中文说明：记录文件后端的根目录，后续读写都基于这个目录。
    def __init__(self, root: Path) -> None:
        self.root = root

    # 中文说明：在根目录下创建父目录并写入文本文件。
    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    # 中文说明：从根目录下读取指定相对路径的文本内容。
    def read(self, path: str) -> str:
        return (self.root / path).read_text(encoding="utf-8")


# 中文说明：组合后端示例，根据路径前缀把读写路由到不同后端。
class CompositeBackend:
    # 中文说明：同时持有内存后端和文件后端，供路由时选择。
    def __init__(self, state: StateBackend, fs: FilesystemBackend) -> None:
        self.state = state
        self.fs = fs

    # 中文说明：写入时 drafts/ 路径走文件后端，其他路径走内存后端。
    def write(self, path: str, content: str) -> None:
        if path.startswith("drafts/"):
            self.fs.write(path, content)
        else:
            self.state.write(path, content)

    # 中文说明：读取时按同样的 drafts/ 前缀规则选择后端。
    def read(self, path: str) -> str:
        if path.startswith("drafts/"):
            return self.fs.read(path)
        return self.state.read(path)


# 中文说明：Backends 示例入口，演示内存、文件和组合路由三种后端行为。
def main() -> None:
    """知识点：Backends 决定 Deep Agents 文件系统表面背后的存储实现。"""
    with tempfile.TemporaryDirectory() as tmp:
        state = StateBackend()
        fs = FilesystemBackend(Path(tmp))
        backend = CompositeBackend(state=state, fs=fs)    # ☀️☀️☀️  这里就是在做路由划分
        backend.write("scratch/todos.md", "- 整理课程目标")
        backend.write("drafts/outline.md", "# Deep Agents 课程大纲")
        assert backend.read("scratch/todos.md").startswith("- 整理")
        assert backend.read("drafts/outline.md").startswith("# Deep")
        result = {
            "concept_plan": get_backend_plan(),
            "state_backend_files": state.files,
            "filesystem_backend_file": backend.read("drafts/outline.md"),
            "routing_rule": "drafts/** -> FilesystemBackend, others -> StateBackend",
        }
    print(pretty_json(result))


if __name__ == "__main__":
    main()
