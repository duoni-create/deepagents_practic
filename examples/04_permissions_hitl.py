from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic.tools import get_permission_policy, pretty_json


# 中文说明：根据路径、动作和策略模拟判断当前操作是允许还是拒绝。
def resolve_permission(path: str, action: str, policy: dict) -> str:
    """用课堂版规则模拟 Deep Agents 文件权限判断。"""
    for rule in policy["filesystem_permissions"]:
        pattern = rule["path"].replace("**", "")
        if path == rule["path"] or path.startswith(pattern):
            access = rule["access"]
            if access == "deny":
                return "deny"
            if action == "read" and access in {"read", "read_write"}:
                return "allow"
            if action == "write" and access == "read_write":
                return "allow"
            return "deny"
    return "deny"


# 中文说明：权限和 HITL 示例入口，验证草稿可写、资料可读、.env 禁止读、删除需审批。
def main() -> None:
    """知识点：权限和人工审批是生产级 Agent 的刹车系统。"""
    permission_demo = get_permission_policy()
    permission_demo["classroom_metaphor"] = "权限像教室门禁，HITL 像老师签字；学生可以练习，但危险动作要先举手。"
    checks = {
        "draft_write": resolve_permission("drafts/course.md", "write", permission_demo),
        "data_read": resolve_permission("data/course_catalog.json", "read", permission_demo),
        "env_read": resolve_permission(".env", "read", permission_demo),
        "delete_file_needs_hitl": permission_demo["interrupt_on"]["delete_file"],
    }
    assert checks == {
        "draft_write": "allow",
        "data_read": "allow",
        "env_read": "deny",
        "delete_file_needs_hitl": True,
    }
    print(pretty_json({"policy": permission_demo, "checks": checks}))


if __name__ == "__main__":
    main()
