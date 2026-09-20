import asyncio

from app.ai.cala import create_learner_context
from app.ai.providers import _decode_json
from app.orchestrator.workflow import _needs_research
from app.schemas.learning import RoadmapPlan
from app.schemas.onboarding import MindsetSubmission


def test_mindset_requires_exactly_five_answers() -> None:
    payload = MindsetSubmission.model_validate({"answers": [{"question_number": number, "answer": "A"} for number in range(1, 6)]})
    assert len(payload.answers) == 5


def test_mindset_rejects_incomplete_answers() -> None:
    try:
        MindsetSubmission.model_validate({"answers": [{"question_number": 1, "answer": "A"}]})
    except ValueError:
        return
    raise AssertionError("incomplete mindset submission should be rejected")


def test_roadmap_output_is_structured() -> None:
    plan = _decode_json('{"title":"ML basics","objective":"Explain learning","nodes":[{"concept":"data","objective":"Describe data","activity_type":"explanation","difficulty":"easy","estimated_minutes":10}]}', RoadmapPlan)
    assert plan.nodes[0].concept == "data"


def test_research_routing_only_for_freshness_needs() -> None:
    assert _needs_research("learn current pricing", "compare recent options") is True
    assert _needs_research("learn fractions", "solve basic problems") is False


def test_cala_builds_context_from_learner_inputs() -> None:
    context = create_learner_context(
        "Learn Python",
        "Understand Python Variables",
        "Beginner and I get confused by reassignment",
        "Video Games",
    )
    assert context.topic.lower() == "python"
    assert "variables" in " ".join(context.concepts).lower()
    assert context.difficulty_level == "very_easy"
    assert any("game" in item.lower() or "video" in item.lower() for item in context.teaching_style)
    assert context.confidence_level == "low"

