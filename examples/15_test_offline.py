from deepagents_practic import build_course_agent, load_settings, run_agent
from deepagents_practic.core_capabilities import CORE_CAPABILITIES
from deepagents_practic.tools import explain_core_capability, estimate_lesson_minutes, get_permission_policy
from ecommerce.tools import check_ecommerce_report_project, define_ecommerce_report_requirements, load_ecommerce_metrics


# 中文说明：验证课程时长估算工具能按章节数和难度算出正确分钟数。
def test_estimate_lesson_minutes() -> None:
    result = estimate_lesson_minutes(4, "进阶")
    assert result["estimated_minutes"] == 180


# 中文说明：验证离线课程 Agent 能被创建并返回包含关键内容的回答。
def test_offline_agent_runs() -> None:
    settings = load_settings()
    agent = build_course_agent(settings)
    answer = run_agent(agent, "设计一个工具调用小实验")
    assert "离线模拟" in answer or "实验" in answer


# 中文说明：验证核心能力清单完整覆盖课程要求的 15 个 Deep Agents 能力点。
def test_core_capabilities_cover_screenshot_terms() -> None:
    expected = {
        "Overview",
        "Models",
        "Context engineering",
        "Backends",
        "Subagents",
        "Async subagents",
        "Human-in-the-loop",
        "Permissions",
        "Memory",
        "Skills",
        "Sandboxes",
        "Interpreters",
        "Profiles",
        "Event streaming",
        "Streaming",
    }
    assert {item.name for item in CORE_CAPABILITIES} == expected


# 中文说明：验证核心能力查询和权限策略工具返回结构化且符合预期的数据。
def test_core_capability_tools_are_structured() -> None:
    profile = explain_core_capability("Profiles")
    assert profile["zh_name"] == "配置档案"
    policy = get_permission_policy()
    assert policy["interrupt_on"]["delete_file"] is True


# 中文说明：验证电商报表项目工具能读取数据、返回需求模块并通过质量检查。
def test_ecommerce_report_project_tools_are_structured() -> None:
    metrics = load_ecommerce_metrics()
    assert "enterprise_ecommerce" in metrics
    requirements = define_ecommerce_report_requirements()
    assert "经营总览" in requirements["report_modules"]
    result = check_ecommerce_report_project("架构 agent 子代理 需求 用户 场景 代码 工具 数据 上线 灰度 审批")
    assert result["score"] == 100
