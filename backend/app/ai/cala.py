from __future__ import annotations

import re
from collections.abc import Iterable

from pydantic import BaseModel, Field


class LearnerContext(BaseModel):
    task: str
    goal: str
    learner_state: str
    interest: str = ""

    topic: str = ""
    concepts: list[str] = Field(default_factory=list)
    difficulty_level: str = "very_easy"
    teaching_style: list[str] = Field(default_factory=list)
    learner_experience: str = "beginner"
    confidence_level: str = "low"
    weaknesses: list[str] = Field(default_factory=list)
    prerequisites: list[str] = Field(default_factory=list)
    learning_objectives: list[str] = Field(default_factory=list)
    content_requirements: list[str] = Field(default_factory=list)
    agent_requirements: dict[str, list[str]] = Field(default_factory=dict)
    adaptation_strategy: str = ""

    def to_prompt_context(self) -> str:
        return (
            "Learner context:\n"
            + "\n".join(
                [
                    f"- task: {self.task}",
                    f"- goal: {self.goal}",
                    f"- learner_state: {self.learner_state}",
                    f"- interest: {self.interest or 'general'}",
                    f"- topic: {self.topic}",
                    f"- concepts: {', '.join(self.concepts) if self.concepts else self.goal}",
                    f"- difficulty_level: {self.difficulty_level}",
                    f"- teaching_style: {', '.join(self.teaching_style)}",
                    f"- weaknesses: {', '.join(self.weaknesses) if self.weaknesses else 'none observed yet'}",
                ]
            )
        )


_NUMBERED_PATTERN = re.compile(r"\b\w{3,}\b")
_TOPIC_HINTS = [
    "python",
    "javascript",
    "java",
    "sql",
    "machine learning",
    "math",
    "statistics",
    "biology",
    "chemistry",
    "physics",
    "data science",
    "frontend",
    "backend",
]


def _normalize_text(value: str | None) -> str:
    return (value or "").strip()


def _infer_topic(task: str, goal: str) -> str:
    text = f"{task} {goal}".lower()
    for hint in _TOPIC_HINTS:
        if hint in text:
            return hint.title() if hint == hint.lower() else hint
    tokens = [token for token in re.split(r"[^a-z0-9]+", text) if token and len(token) > 2]
    return tokens[0].title() if tokens else "General Learning"


def _extract_concepts(goal: str) -> list[str]:
    text = _normalize_text(goal)
    if not text:
        return []
    concepts = [term for term in re.findall(r"\b[a-zA-Z][a-zA-Z0-9_\-]{2,}\b", text) if term.lower() not in {"understand", "learn", "about", "with", "using", "through"}]
    cleaned = []
    seen: set[str] = set()
    for concept in concepts:
        lowered = concept.lower()
        if lowered not in seen:
            seen.add(lowered)
            cleaned.append(concept)
    return cleaned[:5] if cleaned else [text]


def _likely_weaknesses(learner_state: str) -> list[str]:
    text = learner_state.lower()
    patterns = [
        ("confused", "conceptual confusion"),
        ("difficult", "foundational difficulty"),
        ("struggle", "practice gaps"),
        ("weak", "weak areas"),
        ("hard", "harder concepts"),
        ("not sure", "uncertainty"),
        ("beginner", "basic foundations"),
    ]
    weaknesses = []
    for marker, label in patterns:
        if marker in text and label not in weaknesses:
            weaknesses.append(label)
    if not weaknesses:
        return ["foundational comprehension"]
    return weaknesses


def _pick_difficulty(level: str) -> str:
    text = level.lower()
    if any(keyword in text for keyword in ["advanced", "expert", "strong", "confident"]):
        return "medium"
    if any(keyword in text for keyword in ["intermediate", "ready", "comfortable", "understand"]):
        return "easy"
    return "very_easy"


def _build_teaching_style(interest: str) -> list[str]:
    style = ["simple language", "short explanations", "progressive difficulty", "step-by-step examples"]
    if interest and interest.lower() not in {"general", "none", "n/a"}:
        style.append(f"{interest}-themed examples")
    return style


def _detect_experience(learner_state: str) -> str:
    text = learner_state.lower()
    if any(word in text for word in ["expert", "advanced", "proficient", "strong"]):
        return "advanced"
    if any(word in text for word in ["intermediate", "comfortable", "some experience"]):
        return "intermediate"
    return "beginner"


def _detect_confidence(learner_state: str) -> str:
    text = learner_state.lower()
    if any(word in text for word in ["confident", "comfortable", "easy", "clear"]):
        return "high"
    if any(word in text for word in ["hesitant", "struggle", "confused", "hard", "difficult"]):
        return "low"
    return "medium"


def _build_prereqs(topic: str, goal: str) -> list[str]:
    task_goal = f"{topic} {goal}".lower()
    prereqs: list[str] = []
    if "python" in task_goal:
        prereqs.extend(["basic Python syntax", "variables and expressions", "simple problem-solving"])
    elif "math" in task_goal:
        prereqs.extend(["basic arithmetic", "pattern recognition", "equation intuition"])
    elif "machine learning" in task_goal:
        prereqs.extend(["basic statistics", "linear relationships", "data representation"])
    if "variable" in task_goal:
        prereqs.append("value assignment and reuse")
    if not prereqs:
        prereqs.append("core definitions and foundational examples")
    return prereqs[:4]


def _build_objectives(goal: str) -> list[str]:
    clean_goal = goal.strip()
    return [
        f"Understand the core idea behind {clean_goal}.",
        f"Explain {clean_goal} using your own words.",
        f"Apply {clean_goal} in a small practical example.",
    ]


def _build_content_requirements(interest: str) -> list[str]:
    base = [
        "Use beginner-friendly language and clear progression.",
        "Keep the lesson focused on one concept at a time.",
        "Prefer practical examples and short explanations.",
    ]
    if interest and interest.lower() not in {"general", "none", "n/a"}:
        base.append(f"Use {interest}-related examples when they help explain the concept without distracting from the learning objective.")
    return base


def _build_agent_requirements(topic: str, goal: str) -> dict[str, list[str]]:
    concept_name = goal.strip() or "the core concept"
    return {
        "research": [f"Find beginner-friendly, authoritative sources for {topic} and {concept_name}.", "Prioritize clear explanations and official references when available."],
        "teaching": [f"Explain {concept_name} using short steps, simple analogies, and relevant examples.", "Avoid advanced jargon until the learner has enough baseline understanding."],
        "critical_thinking": [f"Ask reasoning questions about {concept_name} and how it changes in different scenarios.", "Check whether the learner understands why, not just what."],
        "real_world": [f"Translate {concept_name} into a practical, low-complexity real-world example.", "Keep the scenario aligned with the learner's level and interest."],
        "quiz": [f"Test recall, reasoning, and quick application of {concept_name} with typed answers.", "Match difficulty to the current mastery level."],
        "evaluation": [f"Review performance across understanding, reasoning, and application of {concept_name}.", "Identify the exact weak concept before recommending remediation."],
    }


def create_learner_context(task: str, goal: str, learner_state: str, interests: str | None = None) -> LearnerContext:
    task_text = _normalize_text(task)
    goal_text = _normalize_text(goal)
    learner_text = _normalize_text(learner_state)
    interest_text = _normalize_text(interests) or "general"

    topic = _infer_topic(task_text, goal_text)
    concepts = _extract_concepts(goal_text) or [goal_text or task_text]
    difficulty = _pick_difficulty(learner_text)
    weaknesses = _likely_weaknesses(learner_text)

    return LearnerContext(
        task=task_text,
        goal=goal_text,
        learner_state=learner_text,
        interest=interest_text,
        topic=topic,
        concepts=concepts,
        difficulty_level=difficulty,
        teaching_style=_build_teaching_style(interest_text),
        learner_experience=_detect_experience(learner_text),
        confidence_level=_detect_confidence(learner_text),
        weaknesses=weaknesses,
        prerequisites=_build_prereqs(topic, goal_text),
        learning_objectives=_build_objectives(goal_text),
        content_requirements=_build_content_requirements(interest_text),
        agent_requirements=_build_agent_requirements(topic, goal_text),
        adaptation_strategy=(
            "Start with the simplest required concept, use interest-based examples to reduce friction, "
            "then expand only after evidence shows the learner can reason, apply, and recall correctly."
        ),
    )
