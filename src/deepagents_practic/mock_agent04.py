from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


# 中文说明：模拟 LangChain 消息对象，让离线 Agent 返回结果时保持类似真实接口的结构。
@dataclass
class MockMessage:
    """模拟 LangChain 消息对象，只保留课堂演示需要的 content。"""

    content: str


# 中文说明：不依赖真实模型的课堂模拟 Agent，用来演示 invoke、stream 和事件流。
class MockDeepAgent:
    """离线模拟 Deep Agent，让代码在未安装依赖、无网络、无模型 Key 时也能跑通。"""

    # 中文说明：初始化模拟 Agent，记录名称、可用工具、系统提示词和子代理清单。
    def __init__(self, name: str, tools: list[Callable[..., Any]], system_prompt: str, subagents: list[dict] | None = None):
        self.name = name
        self.tools = {tool.__name__: tool for tool in tools}
        self.system_prompt = system_prompt
        self.subagents = subagents or []

    # 中文说明：模拟一次 Agent 调用，把用户任务、工具和子代理信息拼成最终回答。
    def invoke(self, payload: dict[str, Any], config: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, list[MockMessage]]:
        """模拟真实 Runnable.invoke 接口，兼容 config 等运行参数。"""
        user_message = payload["messages"][-1]["content"]
        tool_names = "、".join(self.tools.keys()) or "无"
        subagent_names = "、".join(item["name"] for item in self.subagents) or "默认 general-purpose"
        content = (
            f"[离线模拟] {self.name} 已收到任务：{user_message}\n\n"
            f"1. 先用 write_todos 拆成资料、实验、复盘三段。\n"
            f"2. 可用业务工具：{tool_names}。\n"
            f"3. 可委派子代理：{subagent_names}。\n"
            f"4. 覆盖核心能力：Overview、Models、Context engineering、Backends、Subagents、Async subagents、"
            f"HITL、Permissions、Memory、Skills、Sandboxes、Interpreters、Profiles、Event streaming、Streaming。\n"
            f"5. 最终产出：课程目标、章节安排、实验步骤、风险检查。"
        )
        return {"messages": [MockMessage(content=content)]}

    # 中文说明：模拟普通流式输出，依次产出计划、工具调用和最终结果三个阶段。
    def stream(self, payload: dict[str, Any], stream_mode: str = "updates"):
        """模拟 Deep Agents 的流式观察，用于讲解事件流。"""
        user_message = payload["messages"][-1]["content"]
        yield {"plan": f"为任务生成计划：{user_message}"}
        yield {"tool": f"准备调用工具：{', '.join(self.tools.keys()) or '无'}"}
        yield {"final": "完成模拟执行，返回课程草稿。"}

    # 中文说明：模拟结构化事件流，展示计划、子代理启动、工具调用和运行完成事件。
    def stream_events(self, payload: dict[str, Any]):
        """模拟 Deep Agents event streaming：把生命周期拆成可观察事件。"""
        user_message = payload["messages"][-1]["content"]
        yield {"event": "plan.created", "data": {"task": user_message, "todos": ["资料整理", "实验设计", "质量审核"]}}
        yield {"event": "subagent.started", "data": {"name": "research-agent", "mode": "async-ready"}}
        yield {"event": "subagent.started", "data": {"name": "lab-agent", "mode": "async-ready"}}
        yield {"event": "tool.called", "data": {"name": "list_core_capabilities"}}
        yield {"event": "tool.result", "data": {"capability_count": 15}}
        yield {"event": "run.completed", "data": {"output": "核心能力地图已生成。"}}
