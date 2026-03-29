from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def openai_api_key() -> str | None:
    return os.getenv("OPENAI_API_KEY")


def tavily_api_key() -> str | None:
    return os.getenv("TAVILY_API_KEY")


def default_llm_model() -> str:
    return os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
