from fastapi import APIRouter

from .schemas import SummarizeRequest, SummarizeResponse
from ...services.summarizer import SummarizerService

router = APIRouter()
summarizer = SummarizerService()


@router.post("/summaries", response_model=SummarizeResponse)
async def create_summary(payload: SummarizeRequest) -> SummarizeResponse:
    """Trigger the summarization pipeline."""
    summary = await summarizer.summarize(payload)
    return SummarizeResponse(summary=summary.summary, source=summary.source)
