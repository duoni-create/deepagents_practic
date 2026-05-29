from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

# ☀️☀️☀️☀️☀️☀️ 下面这些导入的工具，在这里 tools05.py 没用上，主要是想在这里做一个统一的工具汇总。  agent_factory03.py 那边就直接从 tools05.py 导入所有的工具， 然后开始组装 Agent 可用工具。
# 简单说就是：下面 import 的工具不是给 tools05.py 自己用的，而是让 tools05.py 变成“所有工具函数的统一出口”，方便 agent_factory03.py 从一个地方导入全部工具。
from .core_capabilities06 import (
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
)

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


# 中文说明：读取本地课程素材 JSON，模拟从知识库或资料库检索课程内容。
def load_course_catalog() -> str:
    """读取本地课程素材库，模拟企业内部知识库检索结果。"""
    catalog_path = DATA_DIR / "course_catalog.json"
    return catalog_path.read_text(encoding="utf-8")


# 中文说明：按章节数量和难度估算课程总时长，供 Agent 做课程排期。
def estimate_lesson_minutes(chapter_count: int, difficulty: Literal["入门", "进阶", "项目"] = "进阶") -> dict:
    """根据章节数和难度估算授课时长，供 Agent 做教学排期。"""
    base = {"入门": 35, "进阶": 45, "项目": 60}[difficulty]
    minutes = chapter_count * base
    return {
        "chapter_count": chapter_count,
        "difficulty": difficulty,
        "estimated_minutes": minutes,
        "estimated_hours": round(minutes / 60, 2),
    }


# 中文说明：根据主题生成实验步骤和验收标准，帮助 Agent 输出可落地练习。
def design_lab(topic: str, output: Literal["cli", "web", "report"] = "cli") -> dict:
    """生成实验设计骨架，真实项目中可替换成数据库或模板系统。"""
    return {
        "topic": topic,
        "output": output,
        "steps": [
            "准备 .env 并确认模型配置",
            "定义一个有清晰 docstring 的业务工具函数",
            "用 create_deep_agent 组装模型、工具和系统提示词",
            "运行任务并检查最终消息、工具调用和异常处理",
        ],
        "acceptance": [
            "代码可以通过 compileall",
            "离线模式可以稳定运行",
            "真实模式下不会把 API Key 写进源码",
        ],
    }


# 中文说明：检查课程产出是否包含实验、子代理、权限治理等关键要素并给分。
def quality_check(payload: str) -> dict:
    """对课程产出做轻量质量检查，演示工具返回结构化数据。"""
    score = 70
    issues: list[str] = []
    if "实验" in payload:
        score += 10
    else:
        issues.append("缺少实验环节")
    if "子代理" in payload or "subagent" in payload.lower():
        score += 10
    else:
        issues.append("缺少子代理知识点")
    if "权限" in payload or "审批" in payload:
        score += 10
    else:
        issues.append("缺少治理与安全说明")
    return {"score": min(score, 100), "issues": issues, "raw_length": len(payload)}


# 中文说明：把 Python 对象格式化成缩进 JSON，方便课堂打印和阅读。
def pretty_json(data: object) -> str:
    """让课堂输出更易读。"""
    return json.dumps(data, ensure_ascii=False, indent=2)
