from __future__ import annotations

from .agent import build_ecommerce_report_agent, run_agent
from .tools import (
    check_ecommerce_report_project,
    define_ecommerce_report_requirements,
    design_ecommerce_report_architecture,
    generate_ecommerce_report_spec,
    load_ecommerce_metrics,
    plan_ecommerce_report_launch,
    pretty_json,
)


PROJECT_TASK = """请设计一个企业电商数据报表 Agent 综合项目。
项目必须覆盖：
1. 架构设计图：说明数据源、工具层、主 Agent、子代理、治理层和报表交付；
2. 功能需求：明确用户、场景、报表模块、非功能要求；
3. 代码开发：说明数据文件、工具函数、Agent 编排、流式事件和质量检查；
4. 功能上线：说明开发联调、数据校验、灰度发布、正式上线、运营复盘；
5. 必须体现权限、HITL、事件流观察、质量检查和回滚方案。"""


# 中文说明：调用多个确定性工具，组装电商报表项目的完整材料 JSON。
def build_project_payload() -> str:
    """用确定性工具输出项目材料，保证课堂离线也能讲完整流程。"""
    requirements = define_ecommerce_report_requirements()
    architecture = design_ecommerce_report_architecture()
    spec = generate_ecommerce_report_spec()
    launch = plan_ecommerce_report_launch()
    metrics = load_ecommerce_metrics()
    payload = {
        "project": "企业电商数据报表 Agent",
        "architecture_diagram": "img/ecommerce_report_agent_architecture.svg",
        "sample_metrics": metrics,
        "requirements": requirements,
        "architecture": architecture,
        "development": spec,
        "launch": launch,
    }
    return pretty_json(payload)


# 中文说明：电商报表综合项目入口，依次打印项目材料、Agent 演示、事件流和质量检查。
def main() -> None:
    """综合项目：企业电商数据报表 Agent 的设计、开发和上线流程。"""
    print("--- 项目材料：需求 + 架构 + 开发 + 上线 ---")
    payload = build_project_payload()
    print(payload)

    print("\n--- Agent 任务演示 ---")
    agent = build_ecommerce_report_agent()
    answer = run_agent(agent, PROJECT_TASK)
    print(answer)

    print("\n--- Event streaming 演示 ---")
    for event in agent.stream_events({"messages": [{"role": "user", "content": PROJECT_TASK}]}):
        print(event)

    print("\n--- 项目质量检查 ---")
    print(pretty_json(check_ecommerce_report_project(payload + "\n" + answer)))
