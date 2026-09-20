from __future__ import annotations

from pydantic import BaseModel, Field
import httpx

from app.ai.cala import LearnerContext


class ResearchSource(BaseModel):
    title: str
    url: str
    content: str = Field(default="")
    description: str = Field(default="")
    relevance_score: float = Field(default=0.0)
    task_match: bool = Field(default=False)
    goal_match: bool = Field(default=False)
    concept_match: bool = Field(default=False)
    level_match: bool = Field(default=False)
    interest_match: bool = Field(default=False)
    source_quality: bool = Field(default=False)
    content_completeness: bool = Field(default=False)


class ResearchResult(BaseModel):
    query: str
    sources: list[ResearchSource]


class TavilyResearchService:
    """Tavily boundary for Nova; raw web results never go directly to learners."""

    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key

    def _score_source(self, source: str, learner_context: LearnerContext | None) -> dict[str, bool | float]:
        if learner_context is None:
            return {
                "relevance_score": 0.7,
                "task_match": True,
                "goal_match": True,
                "concept_match": True,
                "level_match": True,
                "interest_match": True,
                "source_quality": True,
                "content_completeness": True,
            }

        lowered = source.lower()
        task_match = bool(learner_context.task.lower() in lowered or learner_context.topic.lower() in lowered)
        goal_match = bool(any(concept.lower() in lowered for concept in learner_context.concepts) or learner_context.goal.lower() in lowered)
        concept_match = bool(any(concept.lower() in lowered for concept in learner_context.concepts)) or goal_match
        level_match = "beginner" in learner_context.learner_state.lower() or "basic" in lowered or "introduction" in lowered or not any(term in lowered for term in ["advanced", "research", "expert"])
        interest_match = bool(learner_context.interest.lower() in lowered or learner_context.interest.lower() == "general" or learner_context.interest.lower() not in lowered)
        source_quality = bool("docs" in lowered or "tutorial" in lowered or "guide" in lowered or "official" in lowered or "documentation" in lowered or "w3schools" in lowered or "stackoverflow" in lowered)
        completeness = bool(len(source) > 220)
        score = sum(
            [
                0.22 if task_match else 0,
                0.22 if goal_match else 0,
                0.22 if concept_match else 0,
                0.12 if level_match else 0,
                0.08 if interest_match else 0,
                0.14 if source_quality else 0,
            ]
        )
        return {
            "relevance_score": round(min(score, 1.0), 2),
            "task_match": task_match,
            "goal_match": goal_match,
            "concept_match": concept_match,
            "level_match": level_match,
            "interest_match": interest_match,
            "source_quality": source_quality,
            "content_completeness": completeness,
        }

    async def search(self, query: str, learner_context: LearnerContext | None = None) -> ResearchResult:
        if not self.api_key:
            return ResearchResult(query=query, sources=[])
        payload = {"api_key": self.api_key, "query": query, "search_depth": "advanced", "max_results": 5, "include_answer": False, "include_raw_content": False}
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post("https://api.tavily.com/search", json=payload)
            response.raise_for_status()
            body = response.json()

        validated_sources: list[ResearchSource] = []
        for item in body.get("results", []):
            url = item.get("url")
            if not url:
                continue
            content = (item.get("content") or "").strip()
            source_text = f"{item.get('title', '')} {content} {item.get('description', '')}"
            metadata = self._score_source(source_text, learner_context)
            if metadata["relevance_score"] < 0.45:
                continue
            validated_sources.append(
                ResearchSource(
                    title=item.get("title", "Untitled source"),
                    url=url,
                    content=content,
                    description=item.get("description", ""),
                    relevance_score=float(metadata["relevance_score"]),
                    task_match=bool(metadata["task_match"]),
                    goal_match=bool(metadata["goal_match"]),
                    concept_match=bool(metadata["concept_match"]),
                    level_match=bool(metadata["level_match"]),
                    interest_match=bool(metadata["interest_match"]),
                    source_quality=bool(metadata["source_quality"]),
                    content_completeness=bool(metadata["content_completeness"]),
                )
            )

        return ResearchResult(query=query, sources=validated_sources[:3])
