# Websage

Websage is a research companion that pairs a FastAPI backend with a Vite/React frontend. The steps below describe how to run the complete experience locally.

## Backend: FastAPI + Uvicorn

1. Install dependencies:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```
2. Start the API server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The backend exposes the `/api/v1/summarize` POST endpoint that the frontend uses to generate summaries.

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
