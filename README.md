# Websage

Websage is a research companion that pairs a FastAPI backend with a Vite/React frontend. The steps below describe how to run the complete experience locally.

## Backend: FastAPI + Uvicorn

1. Configure your LLM credentials (OpenAI by default):
   ```bash
   # Required for OpenAI
   export OPENAI_API_KEY="sk-..."

   # Optional overrides
   export LLM_MODEL="gpt-4.1-mini"   # Any model supported by your provider
   export LLM_TIMEOUT="45"            # Seconds before the request times out

   # Optional: enable the Gemini provider
   export GOOGLE_API_KEY="your-google-key"
   ```
   The backend reads these variables via `backend/app/core/config.py`. If an OpenAI key isn't provided the service falls back to the mock
   provider so you can still iterate locally.
2. Install dependencies:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```
3. Start the API server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The backend now uses the configured provider (OpenAI by default) to serve `/api/v1/summarize` requests with real LLM output.

### Using Gemini instead of OpenAI

If you prefer Gemini, install the optional dependency inside the backend virtual environment and instantiate `GeminiProvider` when wiring up
`SummarizerService` (e.g., inside `backend/app/api/v1/routes.py`).

```bash
pip install google-generativeai
export GOOGLE_API_KEY="your-google-key"
```

```python
from app.services.llm_provider import GeminiProvider
from app.services.summarizer import SummarizerService

summarizer = SummarizerService(provider=GeminiProvider())
```

The rest of the flow remains unchanged.

## Frontend: Vite Dev Server

1. Install dependencies (Node 18+ recommended):
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev -- --host
   ```
   The dev server runs on [http://localhost:5173](http://localhost:5173) and is allowed to call the backend via CORS.

## Triggering a Summary End-to-End

1. Ensure both servers above are running.
2. Visit [http://localhost:5173](http://localhost:5173).
3. Enter the URL you want summarized and customize the prompt if needed.
4. Click **Summarize**. The UI will POST to `http://localhost:8000/api/v1/summarize` and display the returned summary text once the backend responds.

That's it! You're ready to iterate on both sides of the stack with live requests flowing end to end.
