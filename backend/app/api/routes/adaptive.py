"""
API endpoints for the adaptive learning engine.
"""
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.learning.adaptive import (
    ADAPTIVE_THRESHOLDS,
    calculate_mastery,
    diagnose_scenario,
    determine_routing,
    get_next_best_action,
    mastery_band,
    update_concept_scores,
)
from app.models.learner import User
from app.models.learner_concepts import LearnerConcept, LearningGoal

router = APIRouter(tags=["adaptive"])


class ConceptMasteryResponse(BaseModel):
    concept: str
    mastery: float
    accuracy: float
    reasoning_score: float
    application_score: float
    consistency: float
    attempts: int
    mistakes: int
    status: str
    last_reviewed: datetime | None
    next_review: datetime | None
    review_count: int


class NextActionResponse(BaseModel):
    action: str
    concept: str | None
    reason: str
    difficulty: str
    estimated_minutes: int


class AdaptiveRouterResponse(BaseModel):
    route: str
    reason: str
    concept: str
    thresholds: dict[str, float]


class ScenarioResponse(BaseModel):
    scenario: str
    description: str
    avg_mastery: float | None = None
    gap: float | None = None
    concept: str | None = None
    attempts: int | None = None


class ConceptUpsertRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=255)
    concept: str = Field(min_length=1, max_length=255)
    is_correct: bool = Field(default=True)
    accuracy: float | None = Field(default=None, ge=0, le=1)
    reasoning: float | None = Field(default=None, ge=0, le=1)
    application: float | None = Field(default=None, ge=0, le=1)
    consistency: float | None = Field(default=None, ge=0, le=1)


class LearningGoalCreate(BaseModel):
    topic: str = Field(min_length=1, max_length=255)
    goal_description: str = Field(min_length=3, max_length=2000)
    current_level: str = Field(default="beginner")
    motivation: str | None = Field(default=None, max_length=255)


class LearningGoalResponse(BaseModel):
    id: int
    topic: str
    goal_description: str
    current_level: str
    motivation: str | None
    status: str
    created_at: datetime


@router.get("/learning/concepts", response_model=list[ConceptMasteryResponse])
def get_concepts(topic: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    concepts = db.query(LearnerConcept).filter_by(user_id=user.id, topic=topic).order_by(LearnerConcept.mastery).all()
    return [
        ConceptMasteryResponse(
            concept=c.concept, mastery=round(c.mastery, 3), accuracy=round(c.accuracy, 3),
            reasoning_score=round(c.reasoning_score, 3), application_score=round(c.application_score, 3),
            consistency=round(c.consistency, 3), attempts=c.attempts, mistakes=c.mistakes,
            status=c.status, last_reviewed=c.last_reviewed, next_review=c.next_review, review_count=c.review_count,
        )
        for c in concepts
    ]


@router.get("/learning/next-action", response_model=NextActionResponse)
def get_next_action(
    topic: str = "", current_concept: str | None = None, learner_level: str = "beginner",
    db: Session = Depends(get_db), user: User = Depends(get_current_user),
):
    concepts = db.query(LearnerConcept).filter_by(user_id=user.id, topic=topic).all() if topic else []
    concept_scores = {
        c.concept: {"mastery": c.mastery, "accuracy": c.accuracy, "reasoning": c.reasoning_score,
                     "application": c.application_score, "consistency": c.consistency, "attempts": c.attempts}
        for c in concepts
    }
    result = get_next_best_action(
        concept_scores=concept_scores if concept_scores else None,
        current_concept=current_concept, topic=topic or "general", learner_level=learner_level,
    )
    return NextActionResponse(**result)


@router.get("/learning/adaptive-router", response_model=AdaptiveRouterResponse)
def get_routing(concept: str, topic: str = "", db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    concepts = db.query(LearnerConcept).filter_by(user_id=user.id, topic=topic).all() if topic else []
    concept_scores = {
        c.concept: {"mastery": c.mastery, "accuracy": c.accuracy, "reasoning": c.reasoning_score, "application": c.application_score}
        for c in concepts
    }
    result = determine_routing(concept_scores, concept)
    return AdaptiveRouterResponse(route=result["route"], reason=result["reason"], concept=result["concept"], thresholds=ADAPTIVE_THRESHOLDS)


@router.get("/learning/scenario", response_model=ScenarioResponse)
def get_scenario(topic: str = "", db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    concepts = db.query(LearnerConcept).filter_by(user_id=user.id, topic=topic).all() if topic else []
    concept_scores = {
        c.concept: {"accuracy": c.accuracy, "reasoning": c.reasoning_score, "application": c.application_score,
                     "mastery": c.mastery, "attempts": c.attempts}
        for c in concepts
    }
    result = diagnose_scenario(concept_scores)
    return ScenarioResponse(**result)


@router.post("/learning/concepts", status_code=201)
def upsert_concept(
    payload: ConceptUpsertRequest,
    db: Session = Depends(get_db), user: User = Depends(get_current_user),
) -> dict[str, Any]:
    existing = db.query(LearnerConcept).filter_by(user_id=user.id, topic=payload.topic, concept=payload.concept).one_or_none()
    event = {
        "accuracy": payload.accuracy if payload.accuracy is not None else (1.0 if payload.is_correct else 0.0),
        "reasoning": payload.reasoning,
        "application": payload.application,
        "consistency": payload.consistency if payload.consistency is not None else (1.0 if payload.is_correct else 0.0),
        "last_activity_at": datetime.now(),
    }
    if existing:
        new_scores = update_concept_scores(
            {"accuracy": existing.accuracy, "reasoning": existing.reasoning_score, "application": existing.application_score,
             "consistency": existing.consistency}, event,
        )
        existing.accuracy = new_scores["accuracy"]
        existing.reasoning_score = new_scores.get("reasoning", existing.reasoning_score) or 0.0
        existing.application_score = new_scores.get("application", existing.application_score) or 0.0
        existing.consistency = new_scores["consistency"]
        existing.mastery = calculate_mastery(existing.accuracy, existing.reasoning_score, existing.application_score, existing.consistency, existing.review_performance)
        existing.status = mastery_band(existing.mastery)
        existing.attempts += 1
        if payload.is_correct: existing.correct_attempts += 1
        else: existing.mistakes += 1
        db.commit()
        db.refresh(existing)
        return {"concept": existing.concept, "mastery": round(existing.mastery, 3), "status": existing.status, "message": "updated"}
    else:
        mastery = calculate_mastery(event["accuracy"], event.get("reasoning", 0.0), event.get("application", 0.0), event.get("consistency", 0.0), 0.0)
        new_lc = LearnerConcept(
            user_id=user.id, topic=payload.topic, concept=payload.concept, mastery=mastery,
            accuracy=event["accuracy"], reasoning_score=event.get("reasoning", 0.0), application_score=event.get("application", 0.0),
            consistency=event.get("consistency", 0.0), attempts=1,
            correct_attempts=1 if payload.is_correct else 0, mistakes=0 if payload.is_correct else 1,
            last_reviewed=datetime.now(), next_review=datetime.now() + timedelta(days=1),
            review_count=1, review_performance=event["accuracy"], status=mastery_band(mastery),
        )
        db.add(new_lc)
        db.commit()
        db.refresh(new_lc)
        return {"concept": new_lc.concept, "mastery": round(new_lc.mastery, 3), "status": new_lc.status, "message": "created"}


@router.post("/learning/goals", status_code=201, response_model=LearningGoalResponse)
def create_learning_goal(payload: LearningGoalCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    existing = db.query(LearningGoal).filter_by(user_id=user.id, topic=payload.topic).one_or_none()
    if existing:
        existing.goal_description = payload.goal_description
        existing.current_level = payload.current_level
        existing.motivation = payload.motivation
        existing.status = "active"
        db.commit()
        db.refresh(existing)
        return LearningGoalResponse(id=existing.id, topic=existing.topic, goal_description=existing.goal_description, current_level=existing.current_level, motivation=existing.motivation, status=existing.status, created_at=existing.created_at)
    goal = LearningGoal(user_id=user.id, topic=payload.topic, goal_description=payload.goal_description, current_level=payload.current_level, motivation=payload.motivation, status="active")
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return LearningGoalResponse(id=goal.id, topic=goal.topic, goal_description=goal.goal_description, current_level=goal.current_level, motivation=goal.motivation, status=goal.status, created_at=goal.created_at)


@router.get("/learning/goals", response_model=list[LearningGoalResponse])
def get_learning_goals(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    goals = db.query(LearningGoal).filter_by(user_id=user.id).order_by(LearningGoal.created_at.desc()).all()
    return [LearningGoalResponse(id=g.id, topic=g.topic, goal_description=g.goal_description, current_level=g.current_level, motivation=g.motivation, status=g.status, created_at=g.created_at) for g in goals]


@router.get("/learning/demo", response_model=list[ConceptMasteryResponse])
def get_demo_data(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    demo_topic = "Machine Learning"
    demo_concepts = [
        ("Python Basics", 0.92, 0.90, 0.88, 0.95, 0.90),
        ("Statistics", 0.74, 0.72, 0.70, 0.80, 0.75),
        ("Linear Regression", 0.82, 0.80, 0.78, 0.85, 0.80),
        ("Decision Trees", 0.58, 0.55, 0.50, 0.65, 0.55),
        ("Information Gain", 0.42, 0.38, 0.40, 0.45, 0.40),
    ]
    created = []
    for concept, mastery, acc, reasoning, app, cons in demo_concepts:
        existing = db.query(LearnerConcept).filter_by(user_id=user.id, topic=demo_topic, concept=concept).one_or_none()
        if existing:
            existing.mastery = mastery; existing.accuracy = acc; existing.reasoning_score = reasoning
            existing.application_score = app; existing.consistency = cons; existing.attempts = 3
            existing.mistakes = 3 - int(acc * 3); existing.status = mastery_band(mastery); existing.review_count = 2
            db.commit(); db.refresh(existing); created.append(existing)
        else:
            nc = LearnerConcept(user_id=user.id, topic=demo_topic, concept=concept, mastery=mastery, accuracy=acc,
                reasoning_score=reasoning, application_score=app, consistency=cons, attempts=3,
                correct_attempts=3 - int((1 - acc) * 3), mistakes=int((1 - acc) * 3),
                last_reviewed=datetime.now(), next_review=datetime.now() + timedelta(days=1), review_count=2,
                review_performance=acc, status=mastery_band(mastery))
            db.add(nc); db.flush(); created.append(nc)
    if not db.query(LearningGoal).filter_by(user_id=user.id).first():
        db.add(LearningGoal(user_id=user.id, topic=demo_topic, goal_description="Become comfortable building ML models and using them in real projects.", current_level="beginner", motivation="career", status="active"))
        db.commit()
    from app.models.learner import LearningSession, Roadmap, RoadmapNode
    if not db.query(LearningSession).filter_by(user_id=user.id).first():
        session = LearningSession(user_id=user.id, task="Learn Machine Learning Fundamentals", goal="Understand how model weights update through gradient descent", learner_state="I know basic Python and algebra but calculus concepts feel confusing", interests="Robotics and gaming", status="active")
        db.add(session); db.flush()
        roadmap = Roadmap(session_id=session.id, user_id=user.id, title="Machine Learning Fundamentals", objective="From basic concepts to building your first model", status="active")
        db.add(roadmap); db.flush()
        for i, (concept, act_type, diff, est) in enumerate([("Foundations: Python for ML", "explanation", "easy", 10), ("Statistics & Probability", "explanation", "easy", 15), ("Linear Regression", "reasoning", "medium", 20), ("Decision Trees", "application", "medium", 25), ("Information Gain", "reasoning", "hard", 15)], start=1):
            db.add(RoadmapNode(roadmap_id=roadmap.id, position=i, concept=concept, objective=f"Understand {concept}", activity_type=act_type, difficulty=diff, estimated_minutes=est, status="current" if i == 4 else ("completed" if i < 4 else "locked"), is_current=(i == 4)))
        db.commit()
    return [ConceptMasteryResponse(concept=c.concept, mastery=round(c.mastery, 3), accuracy=round(c.accuracy, 3), reasoning_score=round(c.reasoning_score, 3), application_score=round(c.application_score, 3), consistency=round(c.consistency, 3), attempts=c.attempts, mistakes=c.mistakes, status=c.status, last_reviewed=c.last_reviewed, next_review=c.next_review, review_count=c.review_count) for c in created]
