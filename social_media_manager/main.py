from __future__ import annotations

import sys
from pathlib import Path

import typer
from dotenv import load_dotenv

from social_media_manager.crew import run_social_pipeline
from social_media_manager.settings import openai_api_key, repo_root

load_dotenv()

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def run(
    niche: str = typer.Argument(..., help="Topic or niche to research (e.g. 'AI devtools for startups')."),
    platforms: str = typer.Option(
        "LinkedIn, X (Twitter)",
        "--platforms",
        "-p",
        help="Comma-separated list of target platforms.",
    ),
    brand_voice: Path | None = typer.Option(
        None,
        "--brand-voice",
        "-b",
        help="Path to brand_voice.yaml (see config/brand_voice.example.yaml).",
    ),
) -> None:
    """Run the Social Media Manager crew (research → draft → QA)."""
    if not openai_api_key():
        typer.echo("Missing OPENAI_API_KEY. Copy .env.example to .env and set your key.", err=True)
        raise typer.Exit(code=1)

    root = repo_root()
    default_brand = root / "config" / "brand_voice.yaml"
    path = brand_voice if brand_voice is not None else (default_brand if default_brand.is_file() else None)

    result = run_social_pipeline(
        niche=niche,
        platforms=platforms,
        brand_voice_path=path,
    )
    typer.echo(result)


def main() -> None:
    app()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
