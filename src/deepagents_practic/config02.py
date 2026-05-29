from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


# 中文说明：读取项目根目录下的 .env 文件，并把其中的键值写入环境变量。
def load_env_file(path: Path | None = None) -> None:
    """读取 .env 文件，避免课堂环境必须额外安装 python-dotenv。"""
    env_path = path or PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


# 中文说明：集中保存项目运行所需的模型、接口、开关和课程主题配置。
@dataclass(frozen=True)
class Settings:
    """工程集中配置，所有敏感变量都从环境变量或 .env 读取。"""

    deepseek_api_key: str
    deepseek_base_url: str
    deepseek_model: str
    use_real_deepagents: bool
    course_topic: str


# 中文说明：加载 .env 后组装 Settings 对象，供 Agent 工厂和示例入口使用。
def load_settings() -> Settings:
    load_env_file()
    return Settings(
        deepseek_api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        deepseek_base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        deepseek_model=os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash"),
        use_real_deepagents=os.getenv("USE_REAL_DEEPAGENTS", "false").lower() == "true",
        course_topic=os.getenv("COURSE_TOPIC", "Deep Agents 企业级智能体开发"),
    )
