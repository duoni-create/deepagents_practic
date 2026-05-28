from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic import build_course_agent, load_settings, run_agent


# 中文说明：最小运行闭环入口，演示配置读取、Agent 创建、任务执行和结果断言。
def main() -> None:
    """知识点：create_deep_agent 的最小运行闭环。"""
    settings = load_settings()
    agent = build_course_agent(settings)
    answer = run_agent(agent, f"为《{settings.course_topic}》设计 3 个学习目标")
    assert settings.course_topic in answer
    assert "可用业务工具" in answer
    assert "可委派子代理" in answer
    print(answer)
    print("\n[验收通过] Agent 已完成：配置读取 -> Agent 创建 -> invoke 调用 -> 结果检查。")


if __name__ == "__main__":
    main()
