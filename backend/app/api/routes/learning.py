import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.ai.cala import create_learner_context
from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.learning.service import (
    evaluate_assessment_submission,
    evaluate_attempt,
    generate_activity,
    generate_assessment,
    generate_roadmap,
)
from app.models.learner import (
    Achievement,
    ActivityAttempt,
    Assessment,
    AssessmentQuestion,
    LearnerInsight,
    LearnerProfile,
    LearningActivity,
    LearningSession,
    Roadmap,
    RoadmapNode,
    User,
    UserAchievement,
)
from app.schemas.learning import (
    AchievementResponse,
    ActivityResponse,
    AssessmentAttemptResponse,
    AssessmentResponse,
    AssessmentSubmission,
    AttemptCreate,
    AttemptResponse,
    LearnerInsightResponse,
    QuestionResponse,
    RoadmapNodeResponse,
    RoadmapResponse,
    UserStatsResponse,
)

router = APIRouter(tags=["learning"])


class SessionCreate(BaseModel):
    task: str = Field(min_length=2, max_length=2000)
    goal: str = Field(min_length=2, max_length=2000)
    learner_state: str = Field(min_length=2, max_length=2000)
    interests: str = Field(default="", max_length=2000)


@router.post("/sessions", status_code=201)
def create_session(payload: SessionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    learner_context = create_learner_context(payload.task, payload.goal, payload.learner_state, payload.interests)
    session = LearningSession(
        user_id=user.id,
        task=payload.task,
        goal=payload.goal,
        learner_state=payload.learner_state,
        interests=payload.interests,
        learner_context=learner_context.model_dump_json(),
        status="active",
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"id": session.id, "status": session.status, "learner_context": learner_context.model_dump()}


@router.get("/sessions", status_code=200)
def list_sessions(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    sessions = db.query(LearningSession).filter_by(user_id=user.id).order_by(LearningSession.id.desc()).all()
    return [
        {
            "id": s.id,
            "task": s.task,
            "goal": s.goal,
            "status": s.status,
            "created_at": s.created_at,
        }
        for s in sessions
    ]


@router.post("/sessions/{session_id}/roadmap", response_model=RoadmapResponse, status_code=201)
async def create_roadmap(
    session_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> RoadmapResponse:
    session = db.query(LearningSession).filter_by(id=session_id, user_id=user.id).one_or_none()
    if session is None:
        raise HTTPException(status_code=404, detail="Learning session not found")

    existing = db.query(Roadmap).filter_by(session_id=session.id).one_or_none()
    if existing:
        roadmap = existing
    else:
        try:
            roadmap = await generate_roadmap(db, session)
        except RuntimeError as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    nodes = db.query(RoadmapNode).filter_by(roadmap_id=roadmap.id).order_by(RoadmapNode.position).all()
    return RoadmapResponse(
        id=roadmap.id,
        session_id=roadmap.session_id,
        title=roadmap.title,
        objective=roadmap.objective,
        status=roadmap.status,
        nodes=[RoadmapNodeResponse.model_validate(node) for node in nodes],
    )


@router.get("/roadmaps/{roadmap_id}", response_model=RoadmapResponse)
def get_roadmap(roadmap_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    roadmap = db.query(Roadmap).filter_by(id=roadmap_id, user_id=user.id).one_or_none()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    nodes = db.query(RoadmapNode).filter_by(roadmap_id=roadmap.id).order_by(RoadmapNode.position).all()
    return RoadmapResponse(
        id=roadmap.id,
        session_id=roadmap.session_id,
        title=roadmap.title,
        objective=roadmap.objective,
        status=roadmap.status,
        nodes=[RoadmapNodeResponse.model_validate(node) for node in nodes],
    )


@router.post("/roadmaps/{roadmap_id}/nodes/{node_id}/activity", response_model=ActivityResponse, status_code=201)
async def get_or_create_activity(
    roadmap_id: int,
    node_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ActivityResponse:
    roadmap = db.query(Roadmap).filter_by(id=roadmap_id, user_id=user.id).one_or_none()
    node = db.query(RoadmapNode).filter_by(id=node_id, roadmap_id=roadmap_id).one_or_none()
    if roadmap is None or node is None:
        raise HTTPException(status_code=404, detail="Roadmap node not found")

    existing = db.query(LearningActivity).filter_by(node_id=node.id).first()
    if existing:
        return ActivityResponse(
            id=existing.id,
            node_id=existing.node_id,
            activity_type=existing.activity_type,
            prompt=existing.prompt,
            expected_response=existing.expected_response,
        )

    session = db.get(LearningSession, roadmap.session_id)
    try:
        activity = await generate_activity(db, node, session)
        return ActivityResponse(
            id=activity.id,
            node_id=activity.node_id,
            activity_type=activity.activity_type,
            prompt=activity.prompt,
            expected_response=activity.expected_response,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))


@router.post("/activities/{activity_id}/attempts", response_model=AttemptResponse)
async def submit_attempt(
    activity_id: int,
    payload: AttemptCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AttemptResponse:
    activity = db.get(LearningActivity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    session = (
        db.query(LearningSession)
        .join(RoadmapNode, RoadmapNode.id == activity.node_id)
        .join(Roadmap, Roadmap.id == RoadmapNode.roadmap_id)
        .filter(Roadmap.user_id == user.id)
        .first()
    )
    if session is None:
        raise HTTPException(status_code=404, detail="Activity not found for current user")

    try:
        attempt, evaluation, inserted_node = await evaluate_attempt(db, activity, session, user.id, payload.response)
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    inserted_node_resp = RoadmapNodeResponse.model_validate(inserted_node) if inserted_node else None

    return AttemptResponse(
        id=attempt.id,
        activity_id=attempt.activity_id,
        result=attempt.result,
        feedback=attempt.feedback or evaluation.feedback,
        score=evaluation.score,
        clarity_awarded=evaluation.clarity_awarded,
        xp_awarded=evaluation.xp_awarded,
        misconception_detected=evaluation.misconception,
        new_node_inserted=inserted_node is not None,
        new_node=inserted_node_resp,
        created_at=attempt.created_at,
    )


# --- ASSESSMENT ENDPOINTS (ZAYN) ---
@router.post("/roadmaps/{roadmap_id}/assessment", response_model=AssessmentResponse, status_code=201)
async def create_assessment(
    roadmap_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    roadmap = db.query(Roadmap).filter_by(id=roadmap_id, user_id=user.id).one_or_none()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    existing = db.query(Assessment).filter_by(roadmap_id=roadmap.id).first()
    if existing:
        assessment = existing
    else:
        assessment = await generate_assessment(db, roadmap.id, user.id)

    questions = db.query(AssessmentQuestion).filter_by(assessment_id=assessment.id).order_by(AssessmentQuestion.position).all()
    question_resps = []
    for q in questions:
        opts = json.loads(q.options_json) if q.options_json else []
        question_resps.append(
            QuestionResponse(
                id=q.id,
                position=q.position,
                question_text=q.question_text,
                question_type=q.question_type,
                options=opts,
                time_limit=assessment.time_limit_per_question,
            )
        )

    return AssessmentResponse(
        id=assessment.id,
        roadmap_id=assessment.roadmap_id,
        title=assessment.title,
        difficulty=assessment.difficulty,
        time_limit_per_question=assessment.time_limit_per_question,
        questions=question_resps,
    )


@router.post("/assessments/{assessment_id}/submit", response_model=AssessmentAttemptResponse)
async def submit_assessment(
    assessment_id: int,
    payload: AssessmentSubmission,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    assessment = db.query(Assessment).filter_by(id=assessment_id, user_id=user.id).one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    user_answers = {ans.question_id: ans.user_answer for ans in payload.answers}
    return await evaluate_assessment_submission(db, assessment, user.id, user_answers)

# --- STATS, ACHIEVEMENTS & INSIGHTS ---
@router.get("/user/stats", response_model=UserStatsResponse)
def get_user_stats(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    profile = db.query(LearnerProfile).filter_by(user_id=user.id).one_or_none()
    xp = profile.xp if profile else 0
    clarity = profile.clarity if profile else 0
    streak = profile.clarity_streak if profile else 0
    level = (xp // 100) + 1
    title = "Curious Explorer" if level < 3 else ("Concept Connector" if level < 6 else "Clarity Master")

    return UserStatsResponse(xp=xp, clarity=clarity, clarity_streak=streak, level=level, title=title)


@router.get("/user/achievements", response_model=list[AchievementResponse])
def get_user_achievements(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    all_achievements = db.query(Achievement).all()
    user_unlocked = {ua.achievement_id: ua.unlocked_at for ua in db.query(UserAchievement).filter_by(user_id=user.id).all()}

    results = []
    for ach in all_achievements:
        unlocked = ach.id in user_unlocked
        unlocked_at = user_unlocked.get(ach.id)
        results.append(
            AchievementResponse(
                id=ach.id,
                code=ach.code,
                title=ach.title,
                description=ach.description,
                icon=ach.icon,
                xp_reward=ach.xp_reward,
                clarity_reward=ach.clarity_reward,
                unlocked=unlocked,
                unlocked_at=unlocked_at,
            )
        )
    return results


@router.get("/user/insights", response_model=list[LearnerInsightResponse])
def get_user_insights(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    insights = db.query(LearnerInsight).filter_by(user_id=user.id).order_by(LearnerInsight.id.desc()).all()
    if not insights:
        # Default evidence-based starter insights
        return [
            LearnerInsightResponse(id=1, insight_text="You understand concepts faster through visual examples.", category="learning_style", created_at=datetime.now(timezone.utc)),
            LearnerInsightResponse(id=2, insight_text="You recovered quickly from a misconception in your last session.", category="progress", created_at=datetime.now(timezone.utc)),
        ]
    return [LearnerInsightResponse(id=i.id, insight_text=i.insight_text, category=i.category, created_at=i.created_at) for i in insights]
