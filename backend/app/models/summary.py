from dataclasses import dataclass


@dataclass(slots=True)
class Summary:
    """Represents a normalized summary returned by an LLM."""

    text: str
    source_url: str | None = None
