from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic.tools import get_interpreter_plan, pretty_json


# 中文说明：模拟解释器对章节列表做确定性聚合，计算总时长、实验覆盖率和修订标记。
def interpreter_score(chapters: list[dict[str, object]]) -> dict[str, object]:
    """模拟解释器在 Agent 循环内做确定性聚合和评分。"""
    total_minutes = sum(int(item["minutes"]) for item in chapters)
    lab_count = sum(1 for item in chapters if item["has_lab"])
    coverage = round(lab_count / len(chapters), 2)
    return {
        "total_minutes": total_minutes,
        "lab_count": lab_count,
        "lab_coverage": coverage,
        "needs_revision": total_minutes > 300 or coverage < 0.8,
    }


# 中文说明：Interpreters 示例入口，构造章节数据并验证解释器评分结果。
def main() -> None:
    """知识点：Interpreters 在 Agent 循环内部处理结构化数据。"""
    chapters = [
        {"title": "Overview", "minutes": 45, "has_lab": True},
        {"title": "Tools", "minutes": 55, "has_lab": True},
        {"title": "Subagents", "minutes": 65, "has_lab": True},
        {"title": "Production", "minutes": 55, "has_lab": False},
    ]
    result = interpreter_score(chapters)
    assert result["total_minutes"] == 220
    assert result["lab_coverage"] == 0.75
    assert result["needs_revision"] is True
    print(pretty_json({"plan": get_interpreter_plan(), "interpreter_result": result}))


if __name__ == "__main__":
    main()
