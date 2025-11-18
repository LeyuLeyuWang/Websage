from ..api.v1.schemas import SummarizeRequest
from ..models.cache_entry import CacheEntry
from ..repositories.cache import CacheRepository
from .llm_provider import BaseLLMProvider, MockLLMProvider


class SummarizerService:
    def __init__(self, provider: BaseLLMProvider | None = None, cache: CacheRepository | None = None) -> None:
        self.provider = provider or MockLLMProvider()
        self.cache = cache or CacheRepository()

    async def summarize(self, payload: SummarizeRequest) -> CacheEntry:
        cache_key = self.cache.build_key(payload)
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        prompt = payload.prompt
        if payload.url:
            prompt += f"\nSource: {payload.url}"
        if payload.content:
            prompt += f"\nContent: {payload.content[:500]}"

        llm_response = await self.provider.summarize(prompt)
        entry = CacheEntry(key=cache_key, summary=llm_response.text, source=payload.url or "direct")
        await self.cache.set(entry)
        return entry
