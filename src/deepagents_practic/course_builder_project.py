from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from deepagents_practic import build_course_agent, load_settings, run_agent
from deepagents_practic.tools import quality_check, pretty_json


PROJECT_TASK = """请完成一个中型综合项目设计：
项目名：IT 培训课程研发助手。
要求：
1. 面向企业内训老师；
2. 输出 5 小时课程结构；
3. 每章包含理论讲法、代码实验、验收方式；
4. 必须体现 Overview、Models、Context engineering、Backends、Subagents、Async subagents、
   Human-in-the-loop、Permissions、Memory、Skills、Sandboxes、Interpreters、Profiles、
   Event streaming、Streaming；
5. 必须包含工具调用、权限/HITL、流式观察和质量检查。"""

REAL_PROJECT_TASK = """请用一次回答设计一个简版“IT 培训课程研发助手”方案。
要求：
1. 不超过 900 字；
2. 直接输出课程目标、4 个章节、每章实验、验收方式；
3. 必须点名规划、工具、文件系统、子代理、权限/HITL、流式观察；
4. 不要展开长链路研究，不要读写文件，不要委派子代理。"""


# 中文说明：课程研发助手综合项目入口，创建 Agent、执行任务并做质量检查。
def main() -> None:
    """综合项目：串联 Deep Agents 的规划、工具、子代理和质量检查。"""
    settings = load_settings()
    agent = build_course_agent(settings)
    task = REAL_PROJECT_TASK if settings.use_real_deepagents else PROJECT_TASK
    answer = run_agent(agent, task)
    print(answer)
    print("\n--- 质量检查 ---")
    print(pretty_json(quality_check(answer)))


if __name__ == "__main__":
    main()
