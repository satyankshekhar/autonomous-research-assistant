from autonomous_research_analyst.state import ResearchState, ResearchTask


class TaskDecompositionAgent:
    async def run(self, state: ResearchState) -> ResearchState:
        if state.task_graph:
            return state

        state.task_graph = [
            ResearchTask(
                id=f"task-{index}",
                goal_id=goal.id,
                query=f"{state.query} {goal.description}",
            )
            for index, goal in enumerate(state.research_goals, start=1)
        ]
        return state
