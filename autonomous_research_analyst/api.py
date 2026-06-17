from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from autonomous_research_analyst.config import get_settings
from autonomous_research_analyst.graph import ResearchGraph
from autonomous_research_analyst.state import ResearchState

app = FastAPI(
    title="Autonomous Research Analyst",
    description="Multi-agent research pipeline with planning, search, verification, gap analysis, and reports.",
    version="0.1.0",
)

STATIC_DIR = Path(__file__).parent / "static"


class ResearchRequest(BaseModel):
    query: str = Field(min_length=3, examples=["Research quantum computing startups in India"])


class HealthResponse(BaseModel):
    status: str
    live_search_enabled: bool
    max_iterations: int


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        live_search_enabled=bool(settings.tavily_api_key),
        max_iterations=settings.max_iterations,
    )


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return (STATIC_DIR / "index.html").read_text(encoding="utf-8")


@app.post("/research", response_model=ResearchState)
async def research(request: ResearchRequest) -> ResearchState:
    try:
        return await ResearchGraph().run(request.query)
    except Exception as exc:  # pragma: no cover - FastAPI converts this into a client-safe error.
        raise HTTPException(status_code=500, detail=str(exc)) from exc
