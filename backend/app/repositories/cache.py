from collections.abc import MutableMapping

from ..api.v1.schemas import SummarizeRequest
from ..models.cache_entry import CacheEntry


class CacheRepository:
    """In-memory cache placeholder. Replace with Postgres or Redis."""

    def __init__(self, store: MutableMapping[str, CacheEntry] | None = None) -> None:
        self.store = store or {}

    def build_key(self, payload: SummarizeRequest) -> str:
        parts = [payload.prompt]
        if payload.url:
            parts.append(payload.url)
        if payload.content:
            parts.append(payload.content)
        return "|".join(parts)

    async def get(self, key: str) -> CacheEntry | None:
        return self.store.get(key)

    async def set(self, entry: CacheEntry) -> None:
        self.store[entry.key] = entry
