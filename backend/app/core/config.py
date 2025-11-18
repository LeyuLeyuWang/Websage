from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(slots=True)
class Settings:
    """Application configuration sourced from environment variables."""

    openai_api_key: str | None
    google_api_key: str | None
    llm_model: str
    llm_timeout: float


def _coerce_timeout(raw_value: str | None) -> float:
    try:
        return float(raw_value) if raw_value is not None else 30.0
    except (TypeError, ValueError):  # pragma: no cover - defensive
        return 30.0


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        llm_model=os.getenv("LLM_MODEL", "gpt-4.1-mini"),
        llm_timeout=_coerce_timeout(os.getenv("LLM_TIMEOUT")),
    )
