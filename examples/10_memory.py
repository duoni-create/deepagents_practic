from pathlib import Path
import sys
from dataclasses import dataclass, field

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic.tools import get_memory_plan, pretty_json


# 中文说明：课堂版记忆存储，只保存允许长期记住的信息。
@dataclass
class MemoryStore:
    """课堂版长期记忆：只保存允许记住的信息。"""

    values: dict[str, str] = field(default_factory=dict)

    # 中文说明：尝试写入记忆；如果内容包含敏感信息就拒绝保存。
    def remember(self, key: str, value: str, policy: dict) -> bool:
        blocked = ["API Key", "隐私", "错误日志全文"]
        if any(item in value for item in blocked):
            return False
        self.values[key] = value
        return True

    # 中文说明：按 key 读取已经保存的记忆内容。
    def recall(self, key: str) -> str:
        return self.values[key]


# 中文说明：Memory 示例入口，演示可记忆偏好和拒绝保存 API Key。
def main() -> None:
    """知识点：Memory 把跨轮次有价值的信息持久化。"""
    policy = get_memory_plan()
    store = MemoryStore()
    assert store.remember("teacher_pref", "教师偏好：每章都要有实验和验收标准", policy)
    assert not store.remember("secret", "API Key: sk-test", policy)
    assert store.recall("teacher_pref").startswith("教师偏好")
    print(pretty_json({"policy": policy, "memory": store.values}))


if __name__ == "__main__":
    main()
