from fastapi import FastAPI
from .api.v1.routes import router as api_router

app = FastAPI(title="Websage API", version="0.1.0")

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict[str, str]:
  """Health check endpoint."""
  return {"status": "ok"}
