from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic.agent_factory03 import build_course_agent
from deepagents_practic.config02 import load_settings


# 中文说明：子代理示例入口，检查 Agent 是否包含资料、实验和审核三个子代理。
def main() -> None:
    """知识点：子代理适合隔离资料研究、实验设计、审核等复杂上下文。"""
    agent = build_course_agent(load_settings())
    expected = {"research-agent", "lab-agent", "review-agent"}
    actual = {item["name"] for item in agent.subagents}
    assert expected.issubset(actual)
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "请委派资料、实验、审核三个角色，为 Deep Agents 子代理章节做教学设计。",
                }
            ]
        }
    )
    answer = result["messages"][-1].content
    assert "research-agent" in answer
    assert "lab-agent" in answer
    assert "review-agent" in answer
    print(answer)
    print("\n[验收通过] 主 Agent 已识别并暴露 3 个子代理，可用于资料、实验、审核分工。")


if __name__ == "__main__":
    main()
