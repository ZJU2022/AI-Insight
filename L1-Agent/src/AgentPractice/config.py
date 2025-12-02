"""
章节脚本的兼容性配置入口。

推荐做法：
- 在仓库根目录创建 `.env`
- 或者创建 `Agent/config/local.py` 并定义 `OPENAI_API_KEY`/`SERPAPI_API_KEY`

本模块会尝试加载上述配置，并将其写入环境变量，供旧脚本使用。
"""

from __future__ import annotations

import importlib
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


def _load_dotenv() -> None:
    root = Path(__file__).resolve().parents[1]
    env_path = root / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=False)


def _load_local() -> dict[str, Any]:
    try:
        module = importlib.import_module("Agent.config.local")
    except ModuleNotFoundError:
        return {}

    return {
        name: getattr(module, name)
        for name in dir(module)
        if name.isupper()
    }


_load_dotenv()
local_settings = _load_local()

for key, value in local_settings.items():
    os.environ.setdefault(key, value)

for needed in ("OPENAI_API_KEY", "SERPAPI_API_KEY"):
    if needed not in os.environ:
        print(
            f"[Agent.config] 未检测到 {needed}，请参考 README 配置环境变量。",
        )