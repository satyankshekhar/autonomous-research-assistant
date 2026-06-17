from autonomous_research_analyst.state import ResearchState


class QueryPlannerAgent:
    async def run(self, state: ResearchState) -> list[str]:
        queries = []
        for goal in state.missing_goals:
            queries.append(f"{state.query} {goal.description} reliable sources")
            queries.append(f"{state.query} {goal.description} latest updates")
        return [query for query in queries if query not in state.query_history]
