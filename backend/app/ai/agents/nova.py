from app.ai.cala import LearnerContext
from app.core.config import settings
from app.research.tavily import TavilyResearchService


class NovaResearchAgent:
    """NOVA — Research Agent ('The Librarian')
    Purpose: Research current/relevant external information using Tavily.
    Cleans noisy web content and provides clean, structured context to downstream agents.
    """

    def __init__(self) -> None:
        self.tavily_service = TavilyResearchService(settings.tavily_api_key)

    async def execute_research(self, query: str, learner_context: LearnerContext | None = None, stage: str = "learning") -> str:
        if not settings.tavily_api_key:
            return "No web research API key configured. Proceeding with existing knowledge base."

        try:
            result = await self.tavily_service.search(query, learner_context=learner_context)
            if not result.sources:
                return "Web research returned no relevant sources for the learner context. Proceeding with grounded core concepts."

            formatted_sources = []
            for source in result.sources[:3]:
                snippet = source.content[:600].strip()
                relevance = f"relevance={source.relevance_score:.2f}, task_match={source.task_match}, goal_match={source.goal_match}, level_match={source.level_match}"
                formatted_sources.append(
                    f"Source: {source.title}\nURL: {source.url}\nRelevance: {relevance}\nDescription: {source.description or 'Academic / learner-appropriate summary'}\nSummary: {snippet}"
                )

            return "=== NOVA RESEARCH FINDINGS ===\n" + "\n---\n".join(formatted_sources)
        except Exception as e:
            return f"Research attempt encountered issue: {str(e)}. Proceeding with standard curriculum."
