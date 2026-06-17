from typing import Any

from autonomous_research_analyst.state import ResearchState


def to_json(state: ResearchState) -> dict[str, Any]:
    return state.model_dump(mode="json")
