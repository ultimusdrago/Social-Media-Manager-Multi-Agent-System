from __future__ import annotations

import warnings

from crewai_tools import TavilySearchTool

from social_media_manager.settings import tavily_api_key


def build_search_tools() -> list:
    """Return Tavily search tools if TAVILY_API_KEY is set; otherwise empty."""
    if not tavily_api_key():
        warnings.warn(
            "TAVILY_API_KEY is not set. The Trend Researcher will run without live web search. "
            "Set the key in .env for Tavily-backed research.",
            stacklevel=2,
        )
        return []
    return [TavilySearchTool()]
