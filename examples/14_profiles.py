from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deepagents_practic.tools05 import get_profile_plan, pretty_json


PROFILES = {
    "deepseek": {"temperature": 0.2, "tool_visibility": "explicit", "prompt_suffix": "请输出结构化 JSON。"},
    "openai": {"temperature": 0.1, "tool_visibility": "default", "prompt_suffix": "Use concise structured output."},
    "claude": {"temperature": 0.2, "tool_visibility": "profile-managed", "prompt_suffix": "Return a brief plan first."},
}


# 中文说明：根据模型供应商 profile 生成温度、工具可见性和系统提示词配置。
def build_model_config(provider: str, task: str) -> dict[str, object]:
    """用 profile 收敛不同模型供应商的提示词和工具可见性差异。"""
    profile = PROFILES[provider]
    return {
        "provider": provider,
        "temperature": profile["temperature"],
        "tool_visibility": profile["tool_visibility"],
        "system_prompt": f"你是课程研发 Agent。任务：{task}。{profile['prompt_suffix']}",
    }


# 中文说明：Profiles 示例入口，分别生成 deepseek/openai/claude 的配置并打印。
def main() -> None:
    """知识点：Profiles 把不同模型供应商的差异收敛到配置档案。"""
    configs = [build_model_config(provider, "生成 Deep Agents 课程大纲") for provider in PROFILES]
    assert {item["provider"] for item in configs} == {"deepseek", "openai", "claude"}
    assert configs[0]["tool_visibility"] == "explicit"
    print(pretty_json({"plan": get_profile_plan(), "model_configs": configs}))


if __name__ == "__main__":
    main()
