from pathlib import Path
import sys
import asyncio

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic.tools import get_async_subagent_plan, pretty_json


# 中文说明：模拟单个异步子代理处理任务，并返回可合并的结构化结果。
async def run_subagent(name: str, task: str) -> dict[str, str]:
    """模拟异步子代理执行，返回可合并的结构化结果。"""
    await asyncio.sleep(0.01)
    return {"subagent": name, "task": task, "status": "done", "summary": f"{name} 完成：{task}"}


# 中文说明：并发启动多个子代理任务，等待全部完成后合并摘要。
async def orchestrate() -> dict[str, object]:
    plan = get_async_subagent_plan()
    results = await asyncio.gather(
        *[run_subagent(item["subagent"], item["task"]) for item in plan["parallel_tasks"]]
    )
    return {"plan": plan, "results": results, "merged_summary": "；".join(item["summary"] for item in results)}


# 中文说明：异步子代理示例入口，用 asyncio.run 执行并行编排流程。
def main() -> None:
    """知识点：Async subagents 让互不强依赖的子任务并行推进。"""
    result = asyncio.run(orchestrate())
    assert len(result["results"]) == 3
    assert all(item["status"] == "done" for item in result["results"])
    print(pretty_json(result))


if __name__ == "__main__":
    main()
