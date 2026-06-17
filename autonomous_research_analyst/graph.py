from autonomous_research_analyst.agents import (
    EvidenceExtractor,
    GapAnalysisAgent,
    PlannerAgent,
    QueryPlannerAgent,
    SearchAgent,
    TaskDecompositionAgent,
    VerifierAgent,
    WriterAgent,
)
from autonomous_research_analyst.config import Settings, get_settings
from autonomous_research_analyst.providers import build_search_provider
from autonomous_research_analyst.state import ResearchState, ResearchStatus


class ResearchGraph:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        provider = build_search_provider(self.settings)
        self.planner = PlannerAgent()
        self.task_decomposer = TaskDecompositionAgent()
        self.search = SearchAgent(provider)
        self.extractor = EvidenceExtractor()
        self.verifier = VerifierAgent()
        self.gap = GapAnalysisAgent()
        self.query_planner = QueryPlannerAgent()
        self.writer = WriterAgent()

    async def run(self, query: str) -> ResearchState:
        state = ResearchState(query=query, status=ResearchStatus.PLANNING)
        state = await self.planner.run(state)
        state = await self.task_decomposer.run(state)

        follow_up_queries: list[str] | None = None
        for _ in range(self.settings.max_iterations):
            state.iterations += 1
            state = await self.search.run(state, follow_up_queries)
            state = await self.extractor.run(state)
            state = await self.verifier.run(state)
            state = await self.gap.run(state)

            if not state.missing_goals:
                break

            follow_up_queries = await self.query_planner.run(state)
            if not follow_up_queries:
                break

        return await self.writer.run(state)
