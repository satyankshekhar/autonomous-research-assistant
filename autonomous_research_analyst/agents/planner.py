from autonomous_research_analyst.state import ResearchGoal, ResearchState


class PlannerAgent:
    DEFAULT_GOALS = [
        "Identify the most relevant entities, people, or organizations",
        "Find recent developments and current context",
        "Summarize funding, market, or operational signals when available",
        "Identify competitors, alternatives, or adjacent examples",
        "Assess reliability, contradictions, and remaining uncertainty",
    ]

    async def run(self, state: ResearchState) -> ResearchState:
        if state.research_goals:
            return state

        state.research_goals = [
            ResearchGoal(id=f"goal-{index}", description=goal)
            for index, goal in enumerate(self.DEFAULT_GOALS, start=1)
        ]
        return state
