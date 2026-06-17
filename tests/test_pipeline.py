import asyncio

from autonomous_research_analyst.config import Settings
from autonomous_research_analyst.graph import ResearchGraph


def test_research_graph_runs_without_api_keys() -> None:
    settings = Settings(max_iterations=2, search_results_per_query=2)
    state = asyncio.run(ResearchGraph(settings).run("Research quantum computing startups in India"))

    assert state.status == "complete"
    assert state.report.startswith("# Research Report")
    assert state.verified_facts
    assert state.search_runs
    assert state.sources


def test_research_graph_tracks_query_history() -> None:
    settings = Settings(max_iterations=1, search_results_per_query=1)
    state = asyncio.run(ResearchGraph(settings).run("Research AI tooling"))

    assert state.iterations == 1
    assert len(state.query_history) == len(state.task_graph)
