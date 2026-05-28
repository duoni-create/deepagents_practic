from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic.tools import design_lab, estimate_lesson_minutes, pretty_json


# 中文说明：工具调用示例入口，直接调用课程时长估算和实验设计工具并打印结果。
def main() -> None:
    """知识点：工具函数要有类型标注和清晰 docstring，方便模型理解何时调用。"""
    estimate = estimate_lesson_minutes(chapter_count=6, difficulty="进阶")
    lab = design_lab(topic="Deep Agents 工具调用实验", output="cli")
    assert estimate["estimated_minutes"] == 270
    assert lab["output"] == "cli"
    assert len(lab["steps"]) >= 4
    tool_result = {
        "tool_call": "design_lab(topic='Deep Agents 工具调用实验', output='cli')",
        "estimate": estimate,
        "lab": lab,
        "acceptance": "工具返回结构化 dict，Agent 可直接用于后续规划。",
    }
    print(pretty_json(tool_result))


if __name__ == "__main__":
    main()
