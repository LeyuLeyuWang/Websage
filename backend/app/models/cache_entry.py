from dataclasses import dataclass


@dataclass
class CacheEntry:
    key: str
    summary: str
    source: str | None = None
