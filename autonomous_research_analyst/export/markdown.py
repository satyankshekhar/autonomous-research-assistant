from autonomous_research_analyst.state import ResearchState


def to_markdown(state: ResearchState) -> str:
    return state.report
