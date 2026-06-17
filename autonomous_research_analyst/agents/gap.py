from autonomous_research_analyst.state import ResearchState


class GapAnalysisAgent:
    async def run(self, state: ResearchState) -> ResearchState:
        searchable_text = " ".join(fact.fact.lower() for fact in state.verified_facts)
        missing = []

        for goal in state.research_goals:
            keywords = {word.strip(".,") for word in goal.description.lower().split() if len(word) > 4}
            goal.satisfied = bool(keywords.intersection(searchable_text.split()))
            if not goal.satisfied:
                missing.append(goal)

        if not state.verified_facts:
            missing = state.research_goals

        state.missing_goals = missing
        return state
