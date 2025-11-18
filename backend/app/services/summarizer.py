from __future__ import annotations

import json

from ..api.v1.schemas import SummarizeRequest
from ..models.cache_entry import CacheEntry
from ..models.summary import Summary
from ..repositories.cache import CacheRepository
from .llm_provider import LLMProvider, MockLLMProvider, OpenAIProvider


class SummarizerService:
    def __init__(self, provider: LLMProvider | None = None, cache: CacheRepository | None = None) -> None:
        self.provider = provider or self._default_provider()
        self.cache = cache or CacheRepository()

    async def summarize(self, payload: SummarizeRequest) -> CacheEntry:
        cache_key = self.cache.build_key(payload)
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        structured_request = {
            "prompt": payload.prompt,
            "source_url": payload.url,
        }
        serialized_prompt = json.dumps(structured_request, ensure_ascii=False)
        llm_response = await self.provider.generate(serialized_prompt)

        summary = Summary(text=llm_response.text, source_url=payload.url)
        entry = CacheEntry(key=cache_key, summary=summary.text, source=summary.source_url or "direct")
        await self.cache.set(entry)
        return entry

    @staticmethod
    def _default_provider() -> LLMProvider:
        try:
            return OpenAIProvider()
        except Exception:  # pragma: no cover - fallback for local dev
            return MockLLMProvider()
