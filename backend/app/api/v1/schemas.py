from pydantic import BaseModel


class SummarizeRequest(BaseModel):
    url: str
    prompt: str


class SummarizeResponse(BaseModel):
    summary: str
    source: str | None = None
