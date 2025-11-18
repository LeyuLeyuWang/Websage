from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str


class BaseLLMProvider:
    async def summarize(self, prompt: str) -> LLMResponse:  # pragma: no cover - interface
        raise NotImplementedError


class MockLLMProvider(BaseLLMProvider):
    async def summarize(self, prompt: str) -> LLMResponse:
        # Placeholder implementation
        return LLMResponse(text=f"[Mock summary] {prompt[:120]}")
