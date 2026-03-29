from __future__ import annotations

from pathlib import Path

import yaml


def load_brand_voice(path: Path | None) -> str:
    if path is None or not path.is_file():
        return _fallback_brand_voice()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return yaml.dump(data, default_flow_style=False, allow_unicode=True)


def _fallback_brand_voice() -> str:
    return """name: Default Brand
voice:
  tone: [professional, clear, helpful]
  avoid: [clickbait, unverified claims]
audience: General professional audience on social media.
"""
