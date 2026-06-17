from functools import lru_cache
import os
from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    anthropic_api_key: str | None = None
    tavily_api_key: str | None = None
    serper_api_key: str | None = None
    firecrawl_api_key: str | None = None
    langsmith_api_key: str | None = None

    chroma_path: str = ".chroma"
    max_iterations: int = Field(default=3, ge=1, le=10)
    search_results_per_query: int = Field(default=5, ge=1, le=10)
    default_llm_provider: str = "openai"


def _load_env_file(path: Path = Path(".env")) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _get(name: str, default: str | None = None) -> str | None:
    env_file = _load_env_file()
    return os.getenv(name) or env_file.get(name) or default


@lru_cache
def get_settings() -> Settings:
    return Settings(
        openai_api_key=_get("OPENAI_API_KEY"),
        gemini_api_key=_get("GEMINI_API_KEY"),
        anthropic_api_key=_get("ANTHROPIC_API_KEY"),
        tavily_api_key=_get("TAVILY_API_KEY"),
        serper_api_key=_get("SERPER_API_KEY"),
        firecrawl_api_key=_get("FIRECRAWL_API_KEY"),
        langsmith_api_key=_get("LANGSMITH_API_KEY"),
        chroma_path=_get("CHROMA_PATH", ".chroma") or ".chroma",
        max_iterations=int(_get("MAX_ITERATIONS", "3") or "3"),
        search_results_per_query=int(_get("SEARCH_RESULTS_PER_QUERY", "5") or "5"),
        default_llm_provider=_get("DEFAULT_LLM_PROVIDER", "openai") or "openai",
    )
