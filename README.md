# FinSight AI

FinSight is a multi-agent financial-research application. A coordinator routes requests to a Yahoo Finance specialist for current market data and a news specialist for recent, sourced coverage, then combines their results.

## Run locally

1. Create `.env` from `.env.example` and add `GROQ_API_KEY`.
2. Install dependencies: `python -m pip install -r requirements.txt`
3. Start: `uvicorn interface:app --reload`
4. Open `http://127.0.0.1:8000`.

API documentation is available at `/api/docs`; health checks at `/api/health`.

## Deploy with Docker

```bash
docker build -t finsight-ai .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key finsight-ai
```

Set `GROQ_API_KEY` as a secret in your hosting provider. Never commit `.env`. The application is research-only and not investment advice.
