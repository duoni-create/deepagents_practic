from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# ☀️☀️☀️ 直接导入 deepagents_practic 这个项目向外暴露的常用 API，  就直接可以调用他对应的功能，而不需要知道这些函数具体分布在哪些模块里。
from deepagents_practic import build_course_agent, load_settings, run_agent


# 中文说明：最小运行闭环入口，演示配置读取、Agent 创建、任务执行和结果断言。
def main() -> None:
    """知识点：create_deep_agent 的最小运行闭环。"""
    settings = load_settings()
    agent = build_course_agent(settings)
    answer = run_agent(agent, f"为《{settings.course_topic}》设计 3 个学习目标")
    assert settings.course_topic in answer    # ☀️☀️☀️  assert 会检查这个判断：如果为 True：什么都不发生，程序继续往下执行。 如果为 False：抛出 AssertionError，程序停止，说明结果不符合预期。

    # ☀️ 下面两条注释，因为专门针对 MockDeepAgent 实现的，真实调用 API ，可能不会包含这些内容。
    # assert "可用业务工具" in answer
    # assert "可委派子代理" in answer

    print(answer)
    print("\n[验收通过] Agent 已完成：配置读取 -> Agent 创建 -> invoke 调用 -> 结果检查。")


if __name__ == "__main__":
    main()
