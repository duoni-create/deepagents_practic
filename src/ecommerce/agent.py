from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .tools import (
    check_ecommerce_report_project,
    define_ecommerce_report_requirements,
    design_ecommerce_report_architecture,
    generate_ecommerce_report_spec,
    load_ecommerce_metrics,
    plan_ecommerce_report_launch,
)


ECOMMERCE_SYSTEM_PROMPT = """你是企业电商数据报表 Agent。
你负责把经营数据转成可发布的日报方案，必须覆盖需求、架构、开发、上线和回滚。
遇到发布、推送、修改口径等高风险动作时，必须触发人工审批。"""


ECOMMERCE_TOOLS: list[Callable[..., Any]] = [
    load_ecommerce_metrics,
    define_ecommerce_report_requirements,
    design_ecommerce_report_architecture,
    generate_ecommerce_report_spec,
    plan_ecommerce_report_launch,
    check_ecommerce_report_project,
]


# 中文说明：模拟 LangChain 消息对象，用 content 字段承载 Agent 最终回答。
@dataclass
class MockMessage:
    """模拟 LangChain 消息对象，只保留课堂演示需要的 content。"""

    content: str


# 中文说明：企业电商报表 Agent 的离线模拟实现，用于课堂演示完整项目流程。
class MockEcommerceReportAgent:
    """企业电商报表 Agent 的离线模拟，保证课堂不依赖模型服务。"""

    # 中文说明：初始化电商报表 Agent，记录名称、工具、系统提示词和固定子代理。
    def __init__(self, name: str, tools: list[Callable[..., Any]], system_prompt: str):
        self.name = name
        self.tools = {tool.__name__: tool for tool in tools}
        self.system_prompt = system_prompt
        self.subagents = ["metric-agent", "insight-agent", "visual-agent", "release-agent"]

    # 中文说明：模拟一次报表 Agent 执行，把用户任务整理成阶段、工具、子代理和交付物说明。
    def invoke(self, payload: dict[str, Any]) -> dict[str, list[MockMessage]]:
        user_message = payload["messages"][-1]["content"]
        tool_names = "、".join(self.tools.keys())
        subagent_names = "、".join(self.subagents)
        content = (
            f"[离线模拟] {self.name} 已收到任务：{user_message}\n\n"
            f"1. 先拆成需求定义、架构设计、代码开发、功能上线四个阶段。\n"
            f"2. 可用电商报表工具：{tool_names}。\n"
            f"3. 可委派子代理：{subagent_names}。\n"
            f"4. 发布管理层日报、修改指标口径、触发高优先级告警都必须 HITL 审批。\n"
            f"5. 最终产出：架构图说明、功能需求、开发模块、上线计划、回滚方案。"
        )
        return {"messages": [MockMessage(content=content)]}

    # 中文说明：模拟报表项目事件流，展示计划创建、指标分析、审批等待和完成事件。
    def stream_events(self, payload: dict[str, Any]):
        """模拟企业电商报表 Agent 的事件流。"""
        user_message = payload["messages"][-1]["content"]
        yield {"event": "report.plan.created", "data": {"task": user_message, "stages": ["需求", "架构", "开发", "上线"]}}
        yield {"event": "metric_agent.started", "data": {"tool": "load_ecommerce_metrics"}}
        yield {"event": "insight_agent.started", "data": {"focus": "退款率、转化率、缺货风险"}}
        yield {"event": "release_agent.waiting_approval", "data": {"action": "发送管理层日报"}}
        yield {"event": "report.completed", "data": {"output": "企业电商经营日报方案已生成"}}


# 中文说明：创建电商报表离线 Agent，并把报表相关工具注册进去。
def build_ecommerce_report_agent() -> MockEcommerceReportAgent:
    """创建企业电商报表 Agent。"""
    return MockEcommerceReportAgent(
        name="ecommerce-report-agent",
        tools=ECOMMERCE_TOOLS,
        system_prompt=ECOMMERCE_SYSTEM_PROMPT,
    )


# 中文说明：统一调用电商 Agent 的 invoke，并取出最后一条消息内容。
def run_agent(agent: Any, task: str) -> str:
    """统一封装 invoke 调用，兼容后续替换真实 Agent。"""
    result = agent.invoke({"messages": [{"role": "user", "content": task}]})
    return result["messages"][-1].content
