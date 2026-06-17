from autonomous_research_analyst.providers.search import SearchProvider
from autonomous_research_analyst.state import ResearchState, ResearchStatus, SearchRun


class SearchAgent:
    def __init__(self, provider: SearchProvider) -> None:
        self.provider = provider

    async def run(self, state: ResearchState, queries: list[str] | None = None) -> ResearchState:
        state.status = ResearchStatus.SEARCHING
        pending_queries = queries or [task.query for task in state.task_graph if not task.completed]

        for query in pending_queries:
            if query in state.query_history:
                continue
            results = await self.provider.search(query)
            state.raw_search_results.extend(results)
            state.search_runs.append(SearchRun(query=query, provider=self.provider.name, results_count=len(results)))
            state.query_history.append(query)

        for task in state.task_graph:
            if task.query in state.query_history:
                task.completed = True

        return state
