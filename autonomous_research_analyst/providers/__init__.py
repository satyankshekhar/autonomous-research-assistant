from autonomous_research_analyst.config import Settings
from autonomous_research_analyst.providers.search import OfflineSearchProvider, SearchProvider, TavilySearchProvider


def build_search_provider(settings: Settings) -> SearchProvider:
    if settings.tavily_api_key:
        return TavilySearchProvider(settings.tavily_api_key, settings.search_results_per_query)
    return OfflineSearchProvider(settings.search_results_per_query)
