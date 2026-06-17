from collections import defaultdict

from autonomous_research_analyst.state import Contradiction, EvidenceFact, ResearchState, ResearchStatus


class VerifierAgent:
    async def run(self, state: ResearchState) -> ResearchState:
        state.status = ResearchStatus.VERIFYING
        by_source: dict[str, list[EvidenceFact]] = defaultdict(list)
        for fact in state.verified_facts:
            by_source[str(fact.source)].append(fact)

        source_count = max(1, len(by_source))
        for fact in state.verified_facts:
            provider = fact.metadata.get("provider", "")
            source_bonus = 0.15 if provider != "offline" else 0
            agreement_bonus = min(0.2, (source_count - 1) * 0.05)
            fact.confidence = min(0.95, fact.confidence + source_bonus + agreement_bonus)
            fact.support_count = source_count

        state.contradictions = self._detect_simple_contradictions(state.verified_facts)
        state.confidence_scores = {
            "overall": round(
                sum(fact.confidence for fact in state.verified_facts) / max(1, len(state.verified_facts)),
                2,
            ),
            "source_count": float(source_count),
        }
        return state

    def _detect_simple_contradictions(self, facts: list[EvidenceFact]) -> list[Contradiction]:
        money_claims = [
            fact
            for fact in facts
            if fact.metadata.get("provider") != "offline" and ("$" in fact.fact or "funding" in fact.fact.lower())
        ]
        if len(money_claims) < 2:
            return []

        unique_claims = {fact.fact.lower() for fact in money_claims}
        if len(unique_claims) == len(money_claims):
            return [
                Contradiction(
                    topic="funding or financial claims",
                    claims=money_claims[:5],
                    reason="Multiple funding-related claims were found and should be manually reviewed.",
                )
            ]
        return []
