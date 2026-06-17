from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class ResearchStatus(StrEnum):
    CREATED = "created"
    PLANNING = "planning"
    SEARCHING = "searching"
    VERIFYING = "verifying"
    WRITING = "writing"
    COMPLETE = "complete"
    FAILED = "failed"


class ResearchGoal(BaseModel):
    id: str
    description: str
    satisfied: bool = False


class ResearchTask(BaseModel):
    id: str
    goal_id: str
    query: str
    depends_on: list[str] = Field(default_factory=list)
    completed: bool = False


class SearchResult(BaseModel):
    title: str
    url: HttpUrl | str
    snippet: str
    provider: str = "offline"
    score: float = 0.5
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchRun(BaseModel):
    query: str
    provider: str
    results_count: int


class EvidenceFact(BaseModel):
    fact: str
    source: HttpUrl | str
    goal_id: str | None = None
    confidence: float = Field(default=0.5, ge=0, le=1)
    support_count: int = 1
    metadata: dict[str, Any] = Field(default_factory=dict)


class Contradiction(BaseModel):
    topic: str
    claims: list[EvidenceFact]
    reason: str


class ResearchState(BaseModel):
    query: str
    research_goals: list[ResearchGoal] = Field(default_factory=list)
    task_graph: list[ResearchTask] = Field(default_factory=list)
    search_runs: list[SearchRun] = Field(default_factory=list)
    raw_search_results: list[SearchResult] = Field(default_factory=list)
    verified_facts: list[EvidenceFact] = Field(default_factory=list)
    missing_goals: list[ResearchGoal] = Field(default_factory=list)
    query_history: list[str] = Field(default_factory=list)
    research_summary: str = ""
    contradictions: list[Contradiction] = Field(default_factory=list)
    confidence_scores: dict[str, float] = Field(default_factory=dict)
    report: str = ""
    sources: list[str] = Field(default_factory=list)
    iterations: int = 0
    status: ResearchStatus = ResearchStatus.CREATED
