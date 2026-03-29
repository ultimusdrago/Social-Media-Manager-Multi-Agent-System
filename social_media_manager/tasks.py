from __future__ import annotations

from crewai import Task

from social_media_manager.agents import (
    content_strategist,
    editorial_lead,
    trend_researcher,
)


def build_tasks(
    *,
    niche: str,
    platforms: str,
    brand_voice_yaml: str,
    search_tools: list,
    llm,
) -> tuple[Task, Task, Task]:
    """Create sequential tasks: research → draft → QA."""

    hunter = trend_researcher(search_tools, llm)
    writer = content_strategist(llm)
    qa = editorial_lead(llm)

    research = Task(
        description=(
            f"Research niche/topic: {niche}\n\n"
            "Use search tools if available. Produce:\n"
            "1) Top 3–5 timely angles with 1–2 sentences each and why each could resonate.\n"
            "2) For each angle: suggested primary source type (article, paper, repo, official post) "
            "and what to verify.\n"
            "3) A short list of phrases or claims to AVOID (overused, unverifiable, or off-trend).\n"
            "If you cannot verify something, say so explicitly."
        ),
        expected_output=(
            "A structured research memo in Markdown with clear sections and honest uncertainty where needed."
        ),
        agent=hunter,
    )

    draft = Task(
        description=(
            f"Brand voice (YAML):\n```yaml\n{brand_voice_yaml}\n```\n\n"
            f"Target platforms: {platforms}\n\n"
            "Using ONLY the research memo from the previous task as your factual basis, produce:\n"
            "- For each requested platform: complete copy ready to post (or a numbered thread for X).\n"
            "- A one-line 'hook' and a CTA suited to that platform.\n"
            "- If research is thin for a platform, say what is missing instead of inventing details."
        ),
        expected_output=(
            "Platform-labeled drafts in Markdown (e.g., ### LinkedIn, ### X thread). "
            "No fabricated statistics, quotes, or links."
        ),
        agent=writer,
        context=[research],
    )

    review = Task(
        description=(
            "Review the drafts against the research memo and brand voice.\n"
            "Check: tone, factual alignment, repetition, risky or absolute claims, inclusivity, "
            "and platform fit.\n"
            "Output either:\n"
            "A) STATUS: APPROVED — final copy with light edits inline, or\n"
            "B) STATUS: REVISE — ordered list of required changes referencing research gaps."
        ),
        expected_output=(
            "A QA report: APPROVED or REVISE, then final or revision instructions in Markdown."
        ),
        agent=qa,
        context=[research, draft],
    )

    return research, draft, review
