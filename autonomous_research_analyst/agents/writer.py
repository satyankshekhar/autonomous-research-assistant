from autonomous_research_analyst.state import ResearchState, ResearchStatus


class WriterAgent:
    async def run(self, state: ResearchState) -> ResearchState:
        state.status = ResearchStatus.WRITING
        facts = sorted(state.verified_facts, key=lambda fact: fact.confidence, reverse=True)
        sources = []
        lines = [
            f"# Research Report: {state.query}",
            "",
            "## Executive Summary",
            self._summary(state),
            "",
            "## Verified Findings",
        ]

        if facts:
            for fact in facts:
                source = str(fact.source)
                sources.append(source)
                lines.append(f"- {fact.fact} (confidence: {fact.confidence:.2f}) [{len(sources)}]")
        else:
            lines.append("- No verified facts were extracted.")

        lines.extend(["", "## Missing Information"])
        if state.missing_goals:
            lines.extend(f"- {goal.description}" for goal in state.missing_goals)
        else:
            lines.append("- No major gaps detected by the current pipeline.")

        lines.extend(["", "## Contradictions Detected"])
        if state.contradictions:
            lines.extend(f"- {item.topic}: {item.reason}" for item in state.contradictions)
        else:
            lines.append("- No contradictions detected by the current verifier.")

        lines.extend(["", "## Confidence Assessment"])
        lines.append(f"- Overall confidence: {state.confidence_scores.get('overall', 0):.2f}")
        lines.append(f"- Sources reviewed: {int(state.confidence_scores.get('source_count', 0))}")

        lines.extend(["", "## References"])
        unique_sources = list(dict.fromkeys(sources))
        if unique_sources:
            lines.extend(f"{index}. {source}" for index, source in enumerate(unique_sources, start=1))
        else:
            lines.append("No sources available.")

        state.sources = unique_sources
        state.report = "\n".join(lines)
        state.research_summary = self._summary(state)
        state.status = ResearchStatus.COMPLETE
        return state

    def _summary(self, state: ResearchState) -> str:
        fact_count = len(state.verified_facts)
        source_count = len({str(fact.source) for fact in state.verified_facts})
        missing_count = len(state.missing_goals)
        return (
            f"Completed {state.iterations} research iteration(s), extracting {fact_count} fact(s) "
            f"from {source_count} source(s). {missing_count} goal(s) remain partially unresolved."
        )
