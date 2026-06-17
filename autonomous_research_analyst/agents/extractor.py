from autonomous_research_analyst.state import EvidenceFact, ResearchState


class EvidenceExtractor:
    async def run(self, state: ResearchState) -> ResearchState:
        existing = {(fact.fact, str(fact.source)) for fact in state.verified_facts}
        new_facts: list[EvidenceFact] = []

        for result in state.raw_search_results:
            snippet = " ".join(result.snippet.split())
            if not snippet:
                continue
            fact_text = snippet[:280]
            key = (fact_text, str(result.url))
            if key in existing:
                continue
            new_facts.append(
                EvidenceFact(
                    fact=fact_text,
                    source=result.url,
                    confidence=min(0.9, max(0.2, result.score)),
                    metadata={"title": result.title, "provider": result.provider},
                )
            )
            existing.add(key)

        state.verified_facts.extend(new_facts)
        return state
