from __future__ import annotations

from typing import Any

from .config02 import Settings, load_settings
from .mock_agent04 import MockDeepAgent
from .tools05 import (
    design_lab,
    estimate_lesson_minutes,
    explain_core_capability,
    get_async_subagent_plan,
    get_backend_plan,
    get_interpreter_plan,
    get_memory_plan,
    get_permission_policy,
    get_profile_plan,
    get_sandbox_plan,
    get_skill_plan,
    list_core_capabilities,
    load_course_catalog,
    quality_check,
)


COURSE_SYSTEM_PROMPT = """你是资深 IT 教育培训开发老师。
你的任务是把复杂技术拆成学生能理解、能动手、能复盘的课程。
回答时优先给出：学习目标、课堂讲法、实验步骤、常见错误、验收方式。
必须覆盖核心能力：Overview、Models、Context engineering、Backends、Subagents、Async subagents、
Human-in-the-loop、Permissions、Memory、Skills、Sandboxes、Interpreters、Profiles、Event streaming、Streaming。
遇到大任务时先规划，再调用工具或委派子代理，最后给出可执行交付物。"""


CORE_CAPABILITY_TOOLS = [
    list_core_capabilities,
    explain_core_capability,
    get_backend_plan,
    get_async_subagent_plan,
    get_permission_policy,
    get_memory_plan,
    get_skill_plan,
    get_sandbox_plan,
    get_interpreter_plan,
    get_profile_plan,
]


BUSINESS_TOOLS = [
    load_course_catalog,
    estimate_lesson_minutes,
    design_lab,
    quality_check,
]


# 中文说明：真实模型模式下创建 Deep Agents Agent，并配置模型、工具和子代理。
def _build_real_agent(settings: Settings):
    """创建真实 Deep Agents；只有 USE_REAL_DEEPAGENTS=true 时才会调用。"""
    from deepagents import create_deep_agent
    from langchain_openai import ChatOpenAI

    model = ChatOpenAI(
        model=settings.deepseek_model,
        api_key=settings.deepseek_api_key,
        base_url=settings.deepseek_base_url,
        temperature=0.2,
        timeout=60,
        max_retries=1,
        max_completion_tokens=2000,
        # DeepSeek V4 enables thinking mode by default. Current LangChain tool
        # loops do not preserve DeepSeek's reasoning_content field, so disable
        # thinking mode for OpenAI-compatible tool calling.
        extra_body={"thinking": {"type": "disabled"}},
    )
    subagents = [
        {
            "name": "research-agent",
            "description": "整理课程资料、提炼官方文档关键点，并返回可引用的摘要",
            "system_prompt": "你是课程资料研究员，只输出结构化摘要和来源线索。",
            "tools": [load_course_catalog],
        },
        {
            "name": "lab-agent",
            "description": "设计 Python 实验和验收方式",
            "system_prompt": "你是实验设计老师，重点输出步骤、代码入口和验收标准。",
            "tools": [design_lab, estimate_lesson_minutes],
        },
        {
            "name": "review-agent",
            "description": "检查课程内容是否包含实验、治理、安全和复盘",
            "system_prompt": "你是教学质量审核员，指出缺失项并给出修订建议。",
            "tools": [quality_check],
        },
    ]
    return create_deep_agent(
        model=model,
        tools=[*BUSINESS_TOOLS, *CORE_CAPABILITY_TOOLS],
        system_prompt=COURSE_SYSTEM_PROMPT,
        subagents=subagents,
        name="course-builder",
    )


# 中文说明：根据配置开关选择创建真实 Agent 或课堂离线 Mock Agent。
def build_course_agent(settings: Settings | None = None):
    """按配置创建真实或离线 Agent。"""
    settings = settings or load_settings()
    tools = [*BUSINESS_TOOLS, *CORE_CAPABILITY_TOOLS]
    if settings.use_real_deepagents:
        return _build_real_agent(settings)
    return MockDeepAgent(
        name="course-builder",
        tools=tools,
        system_prompt=COURSE_SYSTEM_PROMPT,
        subagents=[
            {"name": "research-agent"},
            {"name": "lab-agent"},
            {"name": "review-agent"},
        ],
    )


# 中文说明：统一执行 Agent 任务，并从返回消息中取出最后的文本结果。
def run_agent(agent: Any, task: str) -> str:
    """统一封装 invoke 调用，兼容真实 Agent 和离线模拟 Agent。"""
    result = agent.invoke(
        {"messages": [{"role": "user", "content": task}]},
        config={"recursion_limit": 40},
    )
    return result["messages"][-1].content
