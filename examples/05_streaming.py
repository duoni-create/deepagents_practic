from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic import build_course_agent, load_settings


# 中文说明：流式输出示例入口，分别演示普通 updates 流和结构化 event streaming。
def main() -> None:
    """知识点：Streaming 看实时更新，Event streaming 看结构化生命周期事件。"""
    agent = build_course_agent(load_settings())
    print("--- streaming updates ---")
    updates = list(agent.stream({"messages": [{"role": "user", "content": "设计 Deep Agents 课堂实验"}]}, stream_mode="updates"))
    assert [next(iter(event)) for event in updates] == ["plan", "tool", "final"]
    for event in updates:
        print(event)
    if hasattr(agent, "stream_events"):
        print("--- event streaming ---")
        events = list(agent.stream_events({"messages": [{"role": "user", "content": "生成核心能力地图"}]}))
        event_names = [event["event"] for event in events]
        assert "tool.called" in event_names
        assert event_names[-1] == "run.completed"
        for event in events:
            print(event)


if __name__ == "__main__":
    main()
