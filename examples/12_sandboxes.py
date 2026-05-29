from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic.tools05 import get_sandbox_plan, pretty_json


# 中文说明：课堂版沙箱对象，把文件操作限制在指定临时目录中。
class Sandbox:
    """课堂版沙箱：只允许在临时目录内写文件，不执行真实危险命令。"""

    # 中文说明：记录并规范化沙箱根目录。
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    # 中文说明：向沙箱内写文件，并阻止使用 ../ 逃逸到沙箱外。
    def write_file(self, relative_path: str, content: str) -> Path:
        target = (self.root / relative_path).resolve()
        if not str(target).startswith(str(self.root)):
            raise PermissionError("禁止写出沙箱目录")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    # 中文说明：模拟执行检查逻辑，返回文件是否存在和大小等信息。
    def run_python_check(self, relative_path: str) -> dict[str, object]:
        target = (self.root / relative_path).resolve()
        return {"path": str(target), "exists": target.exists(), "size": target.stat().st_size}


# 中文说明：Sandboxes 示例入口，验证沙箱内写入成功、越界写入被拦截。
def main() -> None:
    """知识点：Sandboxes 让 Agent 在隔离环境里执行有风险的操作。"""
    with tempfile.TemporaryDirectory() as tmp:
        sandbox = Sandbox(Path(tmp))
        created = sandbox.write_file("reports/daily.md", "# 经营日报草稿")
        check = sandbox.run_python_check("reports/daily.md")
        try:
            sandbox.write_file("../escape.txt", "bad")
            escaped = True
        except PermissionError:
            escaped = False
    assert created.name == "daily.md"
    assert check["exists"] is True
    assert escaped is False
    print(pretty_json({"plan": get_sandbox_plan(), "file_check": check, "escape_blocked": not escaped}))


if __name__ == "__main__":
    main()
