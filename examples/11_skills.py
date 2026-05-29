from pathlib import Path
import sys
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic.tools05 import get_skill_plan, pretty_json


# 中文说明：课程研发技能对象，把目标模板、工作流和验收标准封装起来。
@dataclass(frozen=True)
class CourseBuilderSkill:
    """把课程研发方法论封装成可复用技能。"""

    objective_template: str = "学习目标：理解 {topic} 的核心概念并完成一个可运行实验"
    acceptance_template: str = "验收：能解释概念、运行代码、说明安全边界"

    # 中文说明：把技能应用到指定主题，生成学习目标、流程和验收标准。
    def apply(self, topic: str) -> dict[str, object]:
        return {
            "topic": topic,
            "objective": self.objective_template.format(topic=topic),
            "workflow": ["资料整理", "实验设计", "质量检查", "讲义修订"],
            "acceptance": self.acceptance_template,
        }


# 中文说明：Skills 示例入口，创建技能对象并验证输出结构。
def main() -> None:
    """知识点：Skills 把可复用工作流沉淀为 Agent 可调用的能力包。"""
    skill = CourseBuilderSkill()
    output = skill.apply("Deep Agents Skills")
    assert output["workflow"] == ["资料整理", "实验设计", "质量检查", "讲义修订"]
    assert "Deep Agents Skills" in output["objective"]
    print(pretty_json({"plan": get_skill_plan(), "skill_output": output}))


if __name__ == "__main__":
    main()
