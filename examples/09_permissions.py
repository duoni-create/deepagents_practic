from pathlib import Path
import sys
from fnmatch import fnmatch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic.tools05 import get_permission_policy, pretty_json


# 中文说明：按通配符规则判断指定路径的读写操作是否被权限策略允许。
def can_access(path: str, action: str, policy: dict) -> bool:
    """模拟文件权限匹配：deny 优先，其次判断 read/read_write。"""
    for rule in policy["filesystem_permissions"]:
        if fnmatch(path, rule["path"]):
            if rule["access"] == "deny":
                return False
            if action == "read":
                return rule["access"] in {"read", "read_write"}
            if action == "write":
                return rule["access"] == "read_write"
    return False


# 中文说明：判断某个工具动作是否配置了人工审批拦截。
def needs_human_approval(tool_name: str, policy: dict) -> bool:
    return bool(policy["interrupt_on"].get(tool_name))


# 中文说明：权限示例入口，验证资料读取、草稿写入、密钥拒绝和删除审批。
def main() -> None:
    """知识点：Permissions 用最小权限限制 Agent 的读写边界。"""
    policy = get_permission_policy()
    checks = {
        "read_data": can_access("data/course_catalog.json", "read", policy),
        "write_draft": can_access("drafts/course.md", "write", policy),
        "read_env": can_access(".env", "read", policy),
        "delete_requires_hitl": needs_human_approval("delete_file", policy),
    }
    assert checks == {
        "read_data": True,
        "write_draft": True,
        "read_env": False,
        "delete_requires_hitl": True,
    }
    print(pretty_json({"policy": policy, "checks": checks}))


if __name__ == "__main__":
    main()
