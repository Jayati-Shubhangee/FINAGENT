"""FastAPI entry point for FinSight AI."""
import asyncio, os, time, uuid
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from fin_agent import create_financial_research_team

BASE_DIR, STATIC_DIR = Path(__file__).parent, Path(__file__).parent / "static"
MAX_REQUESTS, WINDOW_SECONDS = 12, 60
requests_by_client, team = defaultdict(deque), None
@asynccontextmanager
async def lifespan(_):
    global team
    if os.getenv("GROQ_API_KEY"): team = create_financial_research_team()
    yield
app = FastAPI(title="FinSight AI", version="1.0.0", lifespan=lifespan, docs_url="/api/docs")
app.mount("/assets", StaticFiles(directory=STATIC_DIR), name="assets")
class ResearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=2000)
    session_id: str | None = Field(default=None, max_length=100)
class ResearchResponse(BaseModel): answer: str; session_id: str
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.update({"X-Content-Type-Options":"nosniff","X-Frame-Options":"DENY","Referrer-Policy":"strict-origin-when-cross-origin","Cache-Control":"no-store"})
    return response
def check_rate_limit(client):
    now, entries = time.monotonic(), requests_by_client[client]
    while entries and now - entries[0] > WINDOW_SECONDS: entries.popleft()
    if len(entries) >= MAX_REQUESTS: raise HTTPException(429, "Rate limit exceeded. Please wait a minute and try again.")
    entries.append(now)
@app.get("/api/health")
async def health(): return {"status":"ok", "agent_ready":team is not None}
@app.post("/api/research", response_model=ResearchResponse)
async def research(payload: ResearchRequest, request: Request):
    if team is None: raise HTTPException(503, "Agent is not configured. Set GROQ_API_KEY and restart the service.")
    check_rate_limit(request.client.host if request.client else "unknown")
    session_id = payload.session_id or str(uuid.uuid4())
    try:
        result = await asyncio.to_thread(team.run, payload.query.strip(), session_id=session_id)
        answer = getattr(result, "content", None)
        if not answer: raise RuntimeError("The agent returned an empty response.")
        return ResearchResponse(answer=str(answer), session_id=session_id)
    except HTTPException: raise
    except Exception as exc: raise HTTPException(502, "Research service could not complete this request. Please try again.") from exc
@app.get("/", include_in_schema=False)
async def frontend(): return FileResponse(STATIC_DIR / "index.html")
