from __future__ import annotations

from pathlib import Path

from crewai import Crew, Process

from social_media_manager.agents import build_llm
from social_media_manager.brand import load_brand_voice
from social_media_manager.tasks import build_tasks
from social_media_manager.tools import build_search_tools


def run_social_pipeline(
    *,
    niche: str,
    platforms: str,
    brand_voice_path: Path | None = None,
) -> str:
    """Run the sequential crew: research → draft → QA. Returns final crew output as string."""
    llm = build_llm()
    search_tools = build_search_tools()
    brand_yaml = load_brand_voice(brand_voice_path)

    research_task, draft_task, review_task = build_tasks(
        niche=niche,
        platforms=platforms,
        brand_voice_yaml=brand_yaml,
        search_tools=search_tools,
        llm=llm,
    )

    agents = [
        research_task.agent,
        draft_task.agent,
        review_task.agent,
    ]

    crew = Crew(
        name="social-media-manager",
        agents=agents,
        tasks=[research_task, draft_task, review_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)
