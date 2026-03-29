# Social-Media-Manager-Multi-Agent-System

A small **marketing-agency-style** pipeline: **Trend Research → Content Strategist → Editorial QA**, implemented with [CrewAI](https://docs.crewai.com).

## Agents

| Role | File | Responsibility |
|------|------|------------------|
| Trend Researcher (“Hunter”) | `social_media_manager/agents.py` | Live search (Tavily when configured), structured brief with sources and uncertainty called out |
| Content Strategist (“Writer”) | same | Platform-native drafts from the research only; brand voice from YAML |
| Editorial Lead (“QA”) | same | Fact/tone/platform check; approve or ordered revision |

## Setup

```bash
cd Social-Media-Manager-Multi-Agent-System
uv venv && source .venv/bin/activate   # or python -m venv .venv
uv pip install -e .
cp .env.example .env                    # add OPENAI_API_KEY; add TAVILY_API_KEY for search
cp config/brand_voice.example.yaml config/brand_voice.yaml
```

## Run

```bash
python -m social_media_manager.main "new AI breakthroughs in developer tooling" -p "LinkedIn, X (Twitter)"
```

Optional: `--brand-voice /path/to/brand_voice.yaml`.
