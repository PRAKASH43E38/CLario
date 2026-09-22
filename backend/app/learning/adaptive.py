"""CLARIO Adaptive Learning Engine — mastery, routing, next-action, scenarios."""
from datetime import datetime, timedelta
from typing import Any

ADAPTIVE_THRESHOLDS = {"weak": 0.40, "developing": 0.60, "proficient": 0.80, "assessment_pass": 0.60}

MASTERY_WEIGHTS = {"accuracy": 0.35, "reasoning": 0.20, "application": 0.20, "consistency": 0.15, "recency": 0.10}

MASTERY_BANDS = [(0.00, 0.39, "weak"), (0.40, 0.59, "developing"), (0.60, 0.79, "proficient"), (0.80, 1.00, "mastered")]

SPACED_REVIEW_INTERVALS = [1, 3, 7, 14, 30]

XP_REWARDS = {"lesson": 10, "practice": 15, "master_concept": 50, "review": 10, "assessment_pass": 25}

DIFFICULTY_LEVELS = ["easy", "medium", "hard", "challenge"]

POSSIBLE_ACTIONS = ["LEARN", "REVIEW", "PRACTICE", "THINK", "APPLY", "ASSESS", "REMEDIATE", "ADVANCE"]


def calculate_mastery(accuracy: float, reasoning: float, application: float, consistency: float, recency: float) -> float:
    w = MASTERY_WEIGHTS
    return w["accuracy"] * accuracy + w["reasoning"] * reasoning + w["application"] * application + w["consistency"] * consistency + w["recency"] * recency


def mastery_band(mastery: float) -> str:
    for low, high, band in MASTERY_BANDS:
        if low <= mastery <= high:
            return band
    return "weak"


def update_concept_scores(current: dict[str, float] | None, event: dict[str, Any]) -> dict[str, float]:
    alpha = 0.3
    if current is None:
        current = {"accuracy": 0.0, "reasoning": 0.0, "application": 0.0, "consistency": 0.0, "recency": 0.0}
    result = {}
    for key in ["accuracy", "reasoning", "application", "consistency"]:
        existing = current.get(key, 0.0)
        new_val = event.get(key, existing)
        result[key] = (1 - alpha) * existing + alpha * new_val if new_val is not None else existing
    now = datetime.now()
    last = event.get("last_activity_at")
    recency = max(0.0, 1.0 - (now - last).total_seconds() / 3600 / 168) if last else 0.0
    result["recency"] = (1 - alpha) * current.get("recency", 0.0) + alpha * recency
    return result


def get_next_best_action(concept_scores: dict[str, dict[str, float]] | None, current_concept: str | None, topic: str, learner_level: str = "beginner") -> dict[str, Any]:
    if concept_scores is None or not concept_scores:
        return {"action": "LEARN", "concept": None, "reason": "No concept data yet — start learning", "difficulty": "easy", "estimated_minutes": 10}
    weakest = None
    weakest_score = 1.0
    for concept, scores in concept_scores.items():
        mastery = scores.get("mastery", 0.0)
        if mastery < weakest_score:
            weakest_score = mastery
            weakest = concept
    if weakest is None:
        return {"action": "LEARN", "concept": current_concept or "New Concept", "reason": "Continue with current learning path", "difficulty": "easy", "estimated_minutes": 10}
    ws = concept_scores[weakest]
    weak_t = ADAPTIVE_THRESHOLDS["weak"]
    dev_t = ADAPTIVE_THRESHOLDS["developing"]
    if weakest_score < weak_t:
        if ws.get("application", 0) < ws.get("accuracy", 0) - 0.15:
            return {"action": "APPLY", "concept": weakest, "reason": f"Application is weak for {weakest} — practice using it", "difficulty": "easy", "estimated_minutes": 8}
        elif ws.get("reasoning", 0) < ws.get("accuracy", 0) - 0.15:
            return {"action": "THINK", "concept": weakest, "reason": f"Reasoning is weak for {weakest} — strengthen understanding", "difficulty": "easy", "estimated_minutes": 8}
        else:
            return {"action": "PRACTICE", "concept": weakest, "reason": f"{weakest} mastery is {weakest_score:.0%} — needs practice", "difficulty": "easy", "estimated_minutes": 8}
    elif weakest_score < dev_t:
        if ws.get("mastery", 0) < 0.5:
            return {"action": "PRACTICE", "concept": weakest, "reason": f"{weakest} is developing — keep practicing", "difficulty": "medium", "estimated_minutes": 10}
        else:
            return {"action": "ASSESS", "concept": weakest, "reason": f"{weakest} is ready for assessment", "difficulty": "medium", "estimated_minutes": 10}
    else:
        return {"action": "ADVANCE", "concept": current_concept or weakest, "reason": f"{weakest} is at {weakest_score:.0%} mastery — ready to advance", "difficulty": "medium", "estimated_minutes": 15}


def determine_routing(concept_scores: dict[str, dict[str, float]] | None, current_concept: str) -> dict[str, Any]:
    if concept_scores is None or current_concept not in concept_scores:
        return {"route": "teaching", "reason": "No prior data — start with teaching", "concept": current_concept}
    cs = concept_scores[current_concept]
    mastery = cs.get("mastery", 0.0)
    accuracy = cs.get("accuracy", 0.0)
    reasoning = cs.get("reasoning", 0.0)
    application = cs.get("application", 0.0)
    wt = ADAPTIVE_THRESHOLDS["weak"]
    at = ADAPTIVE_THRESHOLDS["assessment_pass"]
    dt = ADAPTIVE_THRESHOLDS["developing"]
    if mastery < wt:
        return {"route": "teaching", "reason": f"Mastery {mastery:.0%} below {wt:.0%} — re-teach", "concept": current_concept}
    elif reasoning < at:
        return {"route": "critical_thinking", "reason": f"Reasoning {reasoning:.0%} below {at:.0%} — strengthen reasoning", "concept": current_concept}
    elif application < at:
        return {"route": "application", "reason": f"Application {application:.0%} below threshold — practice application", "concept": current_concept}
    elif accuracy < dt:
        return {"route": "practice", "reason": f"Accuracy {accuracy:.0%} below {dt:.0%} — more practice", "concept": current_concept}
    elif mastery < dt:
        return {"route": "assessment", "reason": f"Mastery {mastery:.0%} — assess before advancing", "concept": current_concept}
    else:
        return {"route": "next_concept", "reason": f"Mastery {mastery:.0%} — conceptually clear, advance", "concept": current_concept}


def diagnose_scenario(concept_scores: dict[str, dict[str, float]]) -> dict[str, Any]:
    if not concept_scores:
        return {"scenario": "beginner", "description": "No prior data — treat as beginner"}
    n = len(concept_scores)
    avg_accuracy = sum(c.get("accuracy", 0) for c in concept_scores.values()) / n
    avg_reasoning = sum(c.get("reasoning", 0) for c in concept_scores.values()) / n
    avg_application = sum(c.get("application", 0) for c in concept_scores.values()) / n
    avg_mastery = sum(c.get("mastery", 0) for c in concept_scores.values()) / n
    wt = ADAPTIVE_THRESHOLDS["weak"]
    pt = ADAPTIVE_THRESHOLDS["proficient"]
    if avg_mastery >= pt and avg_accuracy >= 0.85:
        return {"scenario": "mastered", "description": "High mastery across concepts — advance to next topic", "avg_mastery": avg_mastery}
    if avg_accuracy >= 0.75 and avg_reasoning >= 0.65:
        return {"scenario": "strong_learner", "description": "Strong across the board — increase difficulty", "avg_mastery": avg_mastery}
    if avg_accuracy >= 0.65 and avg_application < 0.50:
        return {"scenario": "theory_strong_application_weak", "description": "Good factual knowledge but poor application — route to Application Agent", "gap": avg_accuracy - avg_application}
    if avg_accuracy >= 0.60 and avg_reasoning < 0.50:
        return {"scenario": "reasoning_weak", "description": "Good factual knowledge but weak reasoning — route to Critical Thinking Agent", "gap": avg_accuracy - avg_reasoning}
    for concept, scores in concept_scores.items():
        if scores.get("attempts", 0) >= 3 and scores.get("mastery", 0) < wt:
            return {"scenario": "repeated_mistake", "description": f"Repeated mistakes on '{concept}' — targeted remediation needed", "concept": concept, "attempts": scores.get("attempts", 0)}
    if avg_mastery < wt:
        return {"scenario": "beginner", "description": "Low mastery across concepts — start with easy teaching", "avg_mastery": avg_mastery}
    return {"scenario": "developing", "description": "Developing mastery — continue structured practice", "avg_mastery": avg_mastery}
