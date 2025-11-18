from pydantic import BaseModel, HttpUrl


class SummarizeRequest(BaseModel):
    url: HttpUrl | None = None
    content: str | None = None
    prompt: str = "Summarize the provided content."


class SummarizeResponse(BaseModel):
    summary: str
    source: str | None = None
