"""Deep Agents 课程实战工程。"""

from .agent_factory03 import build_course_agent, run_agent
from .config02 import Settings, load_settings
from .core_capabilities06 import CORE_CAPABILITIES, explain_core_capability, list_core_capabilities



# ☀️☀️☀️☀️☀️☀️ 包的统一出口，向外暴露常用 API。
# 所以 course_builder_project01.py 可以直接写：  from deepagents_practic import build_course_agent, load_settings, run_agent，  而不用知道这些函数具体分布在哪些模块里。

__all__ = [
    "Settings",
    "load_settings",
    "build_course_agent",
    "run_agent",
    "CORE_CAPABILITIES",
    "list_core_capabilities",
    "explain_core_capability",
]
