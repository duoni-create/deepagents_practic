from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic.tools05 import (
    explain_core_capability,
    get_async_subagent_plan,
    get_backend_plan,
    get_interpreter_plan,
    get_memory_plan,
    get_profile_plan,
    get_sandbox_plan,
    get_skill_plan,
    list_core_capabilities,
    pretty_json,
)


# 中文说明：核心能力索引示例入口，打印 15 个能力点、能力卡片和实现方案。
def main() -> None:
    """知识点：把 Core capabilities 清单和本地示例文件打通。"""
    capabilities = list_core_capabilities()
    project_root = Path(__file__).resolve().parents[1]
    missing_examples = [
        item["example_file"]
        for item in capabilities
        if item["example_file"].startswith("examples/") and not (project_root / item["example_file"]).exists()
    ]
    assert len(capabilities) == 15
    assert not missing_examples
    print("--- core capabilities ---")
    for index, item in enumerate(capabilities, start=1):
        print(f"{index:02d}. {item['name']} / {item['zh_name']} -> {item['example_file']}")

    print("\n--- selected capability cards ---")
    for name in ["Backends", "Sandboxes", "Interpreters", "Profiles", "Event streaming"]:
        print(pretty_json(explain_core_capability(name)))

    print("\n--- implementation plans ---")
    plans = {
        "backends": get_backend_plan(),
        "async_subagents": get_async_subagent_plan(),
        "memory": get_memory_plan(),
        "skills": get_skill_plan(),
        "sandboxes": get_sandbox_plan(),
        "interpreters": get_interpreter_plan(),
        "profiles": get_profile_plan(),
    }
    assert plans["backends"]["choices"][0]["backend"] == "StateBackend"
    assert len(plans["async_subagents"]["parallel_tasks"]) == 3
    print(pretty_json(plans))


if __name__ == "__main__":
    main()
