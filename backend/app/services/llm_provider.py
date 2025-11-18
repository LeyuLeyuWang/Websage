from __future__ import annotations

from dataclasses import dataclass
import asyncio
from typing import Any

from openai import AsyncOpenAI

from ..core.config import get_settings


@dataclass(slots=True)
class LLMResponse:
    text: str


class LLMProvider:
    async def generate(self, text: str) -> LLMResponse:  # pragma: no cover - interface
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    async def generate(self, text: str) -> LLMResponse:
        return LLMResponse(text=f"[Mock summary] {text[:120]}")


class OpenAIProvider(LLMProvider):
    """Concrete provider backed by OpenAI's Responses API."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
        client: AsyncOpenAI | None = None,
        max_output_tokens: int = 600,
    ) -> None:
        settings = get_settings()
        self.api_key = api_key or settings.openai_api_key
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")

        self.model = model or settings.llm_model
        self.timeout = timeout or settings.llm_timeout
        self.max_output_tokens = max_output_tokens
        self.client = client or AsyncOpenAI(api_key=self.api_key)

    async def generate(self, text: str) -> LLMResponse:
        response = await self.client.responses.create(
            model=self.model,
            input=text,
            max_output_tokens=self.max_output_tokens,
            timeout=self.timeout,
        )
        content = self._extract_text(response)
        return LLMResponse(text=content.strip())

    @staticmethod
    def _extract_text(response: Any) -> str:
        output_text = getattr(response, "output_text", None)
        if isinstance(output_text, str) and output_text.strip():
            return output_text

        chunks: list[str] = []
        for output in getattr(response, "output", []) or []:
            for content in getattr(output, "content", []) or []:
                text = getattr(content, "text", None)
                if isinstance(text, str):
                    chunks.append(text)
        return "\n".join(chunks)


class GeminiProvider(LLMProvider):  # pragma: no cover - optional provider
    def __init__(self, api_key: str | None = None, model: str = "gemini-1.5-flash") -> None:
        settings = get_settings()
        self.api_key = api_key or settings.google_api_key
        if not self.api_key:
            raise RuntimeError("GOOGLE_API_KEY is not configured")

        try:
            import google.generativeai as genai
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "google-generativeai is required for the Gemini provider"
            ) from exc

        genai.configure(api_key=self.api_key)
        self._model = genai.GenerativeModel(model)

    async def generate(self, text: str) -> LLMResponse:
        def _generate() -> str:
            response = self._model.generate_content(text)
            if hasattr(response, "text") and response.text:
                return response.text
            candidates = getattr(response, "candidates", None)
            if candidates:
                first = candidates[0]
                parts = getattr(getattr(first, "content", None), "parts", [])
                texts = [getattr(part, "text", "") for part in parts]
                return "\n".join(filter(None, texts))
            return ""

        text_output = await asyncio.to_thread(_generate)
        return LLMResponse(text=text_output.strip())
