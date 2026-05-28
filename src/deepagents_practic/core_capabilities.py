from __future__ import annotations

from dataclasses import asdict, dataclass


# 中文说明：描述一个 Deep Agents 核心能力的名称、中文解释、代码落点和文档链接。
@dataclass(frozen=True)
class CoreCapability:
    """Deep Agents 核心能力的课堂讲解卡片。"""

    name: str
    zh_name: str
    classroom_meaning: str
    code_focus: str
    example_file: str
    doc_url: str


CORE_CAPABILITIES: tuple[CoreCapability, ...] = (
    CoreCapability(
        name="Overview",
        zh_name="总览",
        classroom_meaning="把 Deep Agents 理解成 agent harness：在普通工具调用循环外，内置规划、文件系统、子代理、记忆和治理能力。",
        code_focus="build_course_agent() 统一创建真实或离线 Agent。",
        example_file="examples/01_quickstart.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/overview",
    ),
    CoreCapability(
        name="Models",
        zh_name="模型",
        classroom_meaning="模型是推理引擎，课堂重点不是只会聊天，而是稳定支持 tool calling、结构化输出和低温可重复执行。",
        code_focus="Settings 读取 DeepSeek OpenAI-compatible 配置，_build_real_agent() 创建 ChatOpenAI。",
        example_file="src/deepagents_practic/config.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/quickstart",
    ),
    CoreCapability(
        name="Context engineering",
        zh_name="上下文工程",
        classroom_meaning="决定哪些信息放在当前对话、哪些写入工作文件、哪些进入外部知识库，避免把全部资料硬塞给模型。",
        code_focus="load_course_catalog() 模拟资料检索，工具返回结构化数据供 Agent 摘要。",
        example_file="examples/02_tools.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/overview#context-management",
    ),
    CoreCapability(
        name="Backends",
        zh_name="后端",
        classroom_meaning="后端承载 Deep Agents 暴露给模型的文件系统表面，可选择内存状态、本地磁盘、Store 或组合路由。",
        code_focus="examples/07_backends.py 独立演示 StateBackend、FilesystemBackend、StoreBackend、CompositeBackend 的选择。",
        example_file="examples/07_backends.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/backends",
    ),
    CoreCapability(
        name="Subagents",
        zh_name="子代理",
        classroom_meaning="把资料研究、实验设计、质量审核等专业任务放进隔离上下文，由主 Agent 负责委派和整合。",
        code_focus="agent_factory.py 中配置 research-agent、lab-agent、review-agent。",
        example_file="examples/03_subagents.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/subagents",
    ),
    CoreCapability(
        name="Async subagents",
        zh_name="异步子代理",
        classroom_meaning="多个子任务可并行推进，适合资料检索、实验方案、审核建议互不强依赖的场景。",
        code_focus="examples/08_async_subagents.py 独立演示并行委派和汇总策略。",
        example_file="examples/08_async_subagents.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/subagents",
    ),
    CoreCapability(
        name="Human-in-the-loop",
        zh_name="人工介入",
        classroom_meaning="让敏感工具调用先暂停，由人类批准、拒绝或补充说明，避免 Agent 自动执行高风险动作。",
        code_focus="examples/04_permissions_hitl.py 展示 interrupt_on 配置。",
        example_file="examples/04_permissions_hitl.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/human-in-the-loop",
    ),
    CoreCapability(
        name="Permissions",
        zh_name="权限",
        classroom_meaning="按最小权限控制可读、可写、禁止访问的路径和工具，给生产级 Agent 加边界。",
        code_focus="examples/09_permissions.py 独立演示课堂用文件权限策略。",
        example_file="examples/09_permissions.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/permissions",
    ),
    CoreCapability(
        name="Memory",
        zh_name="记忆",
        classroom_meaning="把跨轮次有价值的信息持久化，而不是期待模型在上下文窗口里长期记住。",
        code_focus="examples/10_memory.py 独立演示线程记忆、课程偏好和长期素材沉淀。",
        example_file="examples/10_memory.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/memory",
    ),
    CoreCapability(
        name="Skills",
        zh_name="技能",
        classroom_meaning="把可复用流程、领域规范和工具组合沉淀成技能，让 Agent 不必每次从零理解工作方法。",
        code_focus="examples/11_skills.py 独立演示课程研发技能的结构。",
        example_file="examples/11_skills.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/skills",
    ),
    CoreCapability(
        name="Sandboxes",
        zh_name="沙箱",
        classroom_meaning="让 Agent 在隔离环境里运行命令、编辑文件、安装依赖，保护宿主机文件、密钥和进程。",
        code_focus="examples/12_sandboxes.py 独立对比课堂离线模拟、本地 shell 和远程沙箱。",
        example_file="examples/12_sandboxes.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/sandboxes",
    ),
    CoreCapability(
        name="Interpreters",
        zh_name="解释器",
        classroom_meaning="在 Agent 循环内部运行轻量代码，用于循环、聚合、排序、校验等结构化数据工作。",
        code_focus="examples/13_interpreters.py 独立说明何时用普通工具、解释器或沙箱。",
        example_file="examples/13_interpreters.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/interpreters",
    ),
    CoreCapability(
        name="Profiles",
        zh_name="配置档案",
        classroom_meaning="为不同模型或供应商封装提示词组装、工具可见性、中间件和默认子代理调整。",
        code_focus="examples/14_profiles.py 独立演示模型差异如何收敛到配置档案。",
        example_file="examples/14_profiles.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/profiles",
    ),
    CoreCapability(
        name="Event streaming",
        zh_name="事件流",
        classroom_meaning="把主 Agent、子代理、工具调用、最终输出拆成可观察事件，方便 UI 展示和调试。",
        code_focus="MockDeepAgent.stream_events() 模拟 plan、subagent、tool、final 事件。",
        example_file="examples/05_streaming.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/event-streaming",
    ),
    CoreCapability(
        name="Streaming",
        zh_name="流式输出",
        classroom_meaning="实时查看 token、工具调用、子代理进度和自定义更新，避免只等最终答案。",
        code_focus="MockDeepAgent.stream() 演示课堂流式观察。",
        example_file="examples/05_streaming.py",
        doc_url="https://docs.langchain.com/oss/python/deepagents/streaming/overview",
    ),
)


# 中文说明：返回全部核心能力卡片，作为课程知识地图和工具调用结果。
def list_core_capabilities() -> list[dict[str, str]]:
    """返回截图中这批 Deep Agents 核心能力的结构化清单。"""
    return [asdict(item) for item in CORE_CAPABILITIES]


# 中文说明：按英文名或中文名查找单个核心能力，未找到时返回可选项提示。
def explain_core_capability(name: str) -> dict[str, str]:
    """按英文或中文名称查询一个核心能力，便于 Agent 在讲义中引用。"""
    needle = name.strip().lower()
    for item in CORE_CAPABILITIES:
        if needle in {item.name.lower(), item.zh_name.lower()}:
            return asdict(item)
    available = ", ".join(item.name for item in CORE_CAPABILITIES)
    return {
        "name": name,
        "error": f"未找到该能力。可选项：{available}",
    }


# 中文说明：给出 Backends 的课堂选择方案，说明不同存储后端适用场景和风险。
def get_backend_plan() -> dict[str, object]:
    """演示 Backends：根据课堂场景选择文件系统后端。"""
    return {
        "concept": "Backends",
        "choices": [
            {"backend": "StateBackend", "use_when": "课堂草稿和单线程临时文件", "risk": "进程结束后不适合长期保存"},
            {"backend": "FilesystemBackend", "use_when": "把课程草稿写入本地目录", "risk": "需要配合权限限制路径"},
            {"backend": "StoreBackend", "use_when": "跨线程或跨课程保存长期资料", "risk": "要设计 namespace 和清理策略"},
            {"backend": "CompositeBackend", "use_when": "不同路径路由到不同存储", "risk": "路由优先级需要清晰"},
        ],
    }


# 中文说明：给出异步子代理拆分方案，说明哪些子任务可以并行执行。
def get_async_subagent_plan() -> dict[str, object]:
    """演示 Async subagents：哪些任务可以并行委派。"""
    return {
        "concept": "Async subagents",
        "parallel_tasks": [
            {"subagent": "research-agent", "task": "整理官方文档和课程素材"},
            {"subagent": "lab-agent", "task": "设计可运行实验和验收方式"},
            {"subagent": "review-agent", "task": "检查安全、治理和教学完整性"},
        ],
        "merge_rule": "主 Agent 等待关键结果后统一消歧、补缺口、生成最终交付物。",
    }


# 中文说明：返回课堂项目的文件权限和 HITL 审批策略，用于演示安全边界。
def get_permission_policy() -> dict[str, object]:
    """演示 Permissions 和 HITL：课堂工程的最小权限策略。"""
    return {
        "filesystem_permissions": [
            {"path": "drafts/**", "access": "read_write", "reason": "允许写课程草稿"},
            {"path": "data/**", "access": "read", "reason": "允许读取课程素材"},
            {"path": ".env", "access": "deny", "reason": "禁止读取密钥文件"},
        ],
        "interrupt_on": {
            "send_email": True,
            "delete_file": True,
            "write_file": {"allowed_decisions": ["approve", "reject"]},
        },
    }


# 中文说明：说明 Agent 记忆应该保存什么、不保存什么，以及可能的存储层次。
def get_memory_plan() -> dict[str, object]:
    """演示 Memory：课程助手应该记住什么、不该记住什么。"""
    return {
        "remember": ["教师偏好的课程结构", "常用验收标准", "已经审核通过的实验模板"],
        "do_not_remember": ["API Key", "学生隐私数据", "临时错误日志全文"],
        "storage_layers": ["thread scratchpad", "course namespace", "long-term material store"],
    }


# 中文说明：说明如何把课程研发流程封装成可复用 Skill。
def get_skill_plan() -> dict[str, object]:
    """演示 Skills：把课程研发流程沉淀为可复用能力。"""
    return {
        "skill": "course-builder-skill",
        "contains": ["课程目标模板", "实验设计步骤", "质量检查 rubric", "HITL 审批清单"],
        "benefit": "换课程主题时复用方法论，而不是每次重新写提示词。",
    }


# 中文说明：说明什么时候需要沙箱，以及课堂模式和生产模式的区别。
def get_sandbox_plan() -> dict[str, object]:
    """演示 Sandboxes：何时需要隔离执行环境。"""
    return {
        "use_when": ["运行学生代码", "安装依赖", "执行 shell 命令", "批量处理文件"],
        "classroom_mode": "本工程默认离线模拟，不执行真实危险命令。",
        "production_rule": "需要 shell 执行时优先用远程沙箱，不直接让 Agent 操作宿主机。",
    }


# 中文说明：说明工具调用、解释器和沙箱三种执行方式分别适合什么任务。
def get_interpreter_plan() -> dict[str, object]:
    """演示 Interpreters：在 Agent 循环内部处理结构化数据。"""
    return {
        "use_tool_calling": "一两个简单外部调用。",
        "use_interpreter": "需要循环、排序、聚合、评分、解析或多次工具组合。",
        "use_sandbox": "需要 shell、文件系统、安装依赖或运行测试。",
    }


# 中文说明：说明 Profiles 如何封装不同模型供应商的提示词和工具可见性差异。
def get_profile_plan() -> dict[str, object]:
    """演示 Profiles：把模型差异封装成可维护配置。"""
    return {
        "profile_fields": ["prompt assembly", "tool visibility", "middleware", "default subagents"],
        "classroom_example": "DeepSeek 演示使用低温度和清晰工具描述；OpenAI/Claude 可通过 profile 适配默认提示词和工具可见性。",
        "benefit": "换模型时尽量少改业务代码。",
    }
