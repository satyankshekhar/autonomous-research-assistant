from abc import ABC, abstractmethod

import httpx

from autonomous_research_analyst.state import SearchResult


class SearchProvider(ABC):
    name: str

    @abstractmethod
    async def search(self, query: str) -> list[SearchResult]:
        """Return search results for a query."""


class OfflineSearchProvider(SearchProvider):
    name = "offline"

    def __init__(self, max_results: int = 5) -> None:
        self.max_results = max_results

    async def search(self, query: str) -> list[SearchResult]:
        topics = [
            "background",
            "recent developments",
            "key organizations",
            "funding and market context",
            "risks and open questions",
        ]
        return [
            SearchResult(
                title=f"Offline research note: {topic}",
                url=f"offline://{query.replace(' ', '-').lower()}/{index}",
                snippet=f"Placeholder evidence for '{query}' covering {topic}. Add TAVILY_API_KEY for live web evidence.",
                provider=self.name,
                score=0.35,
            )
            for index, topic in enumerate(topics[: self.max_results], start=1)
        ]


class TavilySearchProvider(SearchProvider):
    name = "tavily"

    def __init__(self, api_key: str, max_results: int = 5) -> None:
        self.api_key = api_key
        self.max_results = max_results

    async def search(self, query: str) -> list[SearchResult]:
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": self.max_results,
            "include_answer": False,
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post("https://api.tavily.com/search", json=payload)
            response.raise_for_status()

        data = response.json()
        results = data.get("results", [])
        return [
            SearchResult(
                title=item.get("title") or "Untitled source",
                url=item.get("url") or "",
                snippet=item.get("content") or "",
                provider=self.name,
                score=float(item.get("score") or 0.5),
                metadata={"raw": item},
            )
            for item in results
        ]
