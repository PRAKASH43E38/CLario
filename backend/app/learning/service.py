import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.ai.agents import (
    AyanReasoningAgent,
    ElaraEvaluationAgent,
    KiraApplicationAgent,
    MiraTeachingAgent,
    ZaynQuizAgent,
)
from app.models.learner import (
    Achievement,
    ActivityAttempt,
    Assessment,
    AssessmentAttempt,
    AssessmentQuestion,
    LearnerInsight,
    LearnerProfile,
    LearningActivity,
    LearningEvidence,
    LearningSession,
    Misconception,
    Roadmap,
    RoadmapNode,
    UserAchievement,
)
from app.orchestrator.workflow import run_roadmap_workflow
from app.schemas.learning import ActivityPlan, AssessmentAttemptResponse, EvaluationPlan, RoadmapPlan


async def generate_roadmap(db: Session, session: LearningSession) -> Roadmap:
    state = await run_roadmap_workflow(session)
    plan: RoadmapPlan = state["roadmap_plan"]
    roadmap = Roadmap(
        session_id=session.id,
        user_id=session.user_id,
        title=plan.title,
        objective=plan.objective,
        status="active",
    )
    db.add(roadmap)
    db.flush()

    for position, node_plan in enumerate(plan.nodes, start=1):
        db.add(
            RoadmapNode(
                roadmap_id=roadmap.id,
                position=position,
                concept=node_plan.concept,
                objective=node_plan.objective,
                activity_type=node_plan.activity_type,
                difficulty=node_plan.difficulty,
                estimated_minutes=node_plan.estimated_minutes,
                status="current" if position == 1 else "locked",
                is_current=(position == 1),
            )
        )
    db.commit()
    db.refresh(roadmap)
    return roadmap


async def generate_activity(db: Session, node: RoadmapNode, session: LearningSession) -> LearningActivity:
    activity_type = node.activity_type.lower()

    if activity_type == "reasoning":
        agent = AyanReasoningAgent()
        plan: ActivityPlan = await agent.generate_reasoning_task(node.concept, node.objective, session.learner_state)
    elif activity_type == "application":
        agent = KiraApplicationAgent()
        plan: ActivityPlan = await agent.generate_application_task(node.concept, node.objective, session.learner_state, session.interests)
    elif activity_type == "misconception_repair":
        agent = MiraTeachingAgent()
        # Find latest misconception for context
        latest_misc = db.query(Misconception).filter_by(user_id=session.user_id, concept=node.concept).order_by(Misconception.id.desc()).first()
        misc_text = latest_misc.description if latest_misc else "Concept confusion"
        plan: ActivityPlan = await agent.generate_misconception_repair(node.concept, misc_text, session.learner_state)
    else:
        # Default: Mira explanation / practice
        agent = MiraTeachingAgent()
        plan: ActivityPlan = await agent.generate_explanation(node.concept, node.objective, session.learner_state, session.interests)

    activity = LearningActivity(
        node_id=node.id,
        activity_type=plan.activity_type,
        prompt=plan.prompt,
        expected_response=plan.expected_response,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


async def evaluate_attempt(
    db: Session,
    activity: LearningActivity,
    session: LearningSession,
    user_id: int,
    response: str,
) -> tuple[ActivityAttempt, EvaluationPlan, RoadmapNode | None]:
    node = db.get(RoadmapNode, activity.node_id)
    elara = ElaraEvaluationAgent()
    plan: EvaluationPlan = await elara.evaluate_response(
        node.concept,
        node.objective,
        activity.prompt,
        activity.expected_response,
        response,
    )

    attempt = ActivityAttempt(
        activity_id=activity.id,
        user_id=user_id,
        response=response,
        result=plan.result,
        feedback=plan.feedback,
    )
    db.add(attempt)

    profile = db.query(LearnerProfile).filter_by(user_id=user_id).one_or_none()
    if profile:
        profile.xp += plan.xp_awarded
        profile.clarity = min(100, profile.clarity + plan.clarity_awarded)
        if plan.result == "correct":
            profile.clarity_streak += 1
        else:
            profile.clarity_streak = 0

    # Store learning evidence
    db.add(
        LearningEvidence(
            user_id=user_id,
            session_id=session.id,
            concept=node.concept,
            evidence_type=f"activity_{node.activity_type}",
            score=plan.score,
            notes=plan.feedback,
        )
    )

    # Dynamic Roadmap Mutation & Misconception Handling
    inserted_node: RoadmapNode | None = None
    if plan.misconception or plan.result == "needs_support":
        # Record misconception
        misc = Misconception(
            user_id=user_id,
            session_id=session.id,
            concept=node.concept,
            description=plan.misconception or plan.feedback,
            status="detected",
        )
        db.add(misc)

        # Shift downstream nodes position by +1 to insert misconception repair node
        roadmap_nodes = db.query(RoadmapNode).filter_by(roadmap_id=node.roadmap_id).order_by(RoadmapNode.position).all()
        for rn in roadmap_nodes:
            if rn.position > node.position:
                rn.position += 1

        inserted_node = RoadmapNode(
            roadmap_id=node.roadmap_id,
            position=node.position + 1,
            concept=f"Misconception Repair: {node.concept}",
            objective=f"Clear up confusion regarding {node.concept}",
            activity_type="misconception_repair",
            difficulty=node.difficulty,
            estimated_minutes=5,
            status="current",
            is_current=True,
        )
        node.is_current = False
        db.add(inserted_node)
    elif plan.result == "correct":
        # Mark current node as completed and unlock next node
        node.status = "completed"
        node.is_current = False

        next_node = db.query(RoadmapNode).filter_by(roadmap_id=node.roadmap_id, position=node.position + 1).first()
        if next_node:
            next_node.status = "unlocked"
            next_node.is_current = True

    # Check and trigger achievements
    await check_and_award_achievements(db, user_id, profile, plan.result, plan.misconception is not None)

    db.commit()
    db.refresh(attempt)
    return attempt, plan, inserted_node


async def generate_assessment(db: Session, roadmap_id: int, user_id: int) -> Assessment:
    roadmap = db.get(Roadmap, roadmap_id)
    zayn = ZaynQuizAgent()
    plan = await zayn.generate_assessment(roadmap.title, roadmap.objective, difficulty="medium")

    assessment = Assessment(
        session_id=roadmap.session_id,
        roadmap_id=roadmap.id,
        user_id=user_id,
        title=plan.title,
        difficulty=plan.difficulty,
        time_limit_per_question=plan.time_limit_per_question,
    )
    db.add(assessment)
    db.flush()

    for q in plan.questions:
        db.add(
            AssessmentQuestion(
                assessment_id=assessment.id,
                position=q.position,
                question_text=q.question_text,
                question_type=q.question_type,
                options_json=json.dumps(q.options),
                correct_answer=q.correct_answer,
                explanation=q.explanation,
            )
        )

    db.commit()
    db.refresh(assessment)
    return assessment


async def evaluate_assessment_submission(
    db: Session,
    assessment: Assessment,
    user_id: int,
    user_answers: dict[int, str],
) -> AssessmentAttemptResponse:
    questions = db.query(AssessmentQuestion).filter_by(assessment_id=assessment.id).order_by(AssessmentQuestion.position).all()
    correct_count = 0

    for q in questions:
        user_ans = user_answers.get(q.id, "").strip()
        if user_ans and user_ans.lower() == q.correct_answer.strip().lower():
            correct_count += 1

    total_q = len(questions) or 5
    score_pct = int((correct_count / total_q) * 100)
    xp_awarded = correct_count * 20
    clarity_awarded = correct_count * 5

    feedback = f"You answered {correct_count} out of {total_q} questions correctly ({score_pct}%)."
    recommendation = "progress" if score_pct >= 80 else ("practice" if score_pct >= 50 else "revisit")

    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        user_id=user_id,
        score=score_pct,
        total_questions=total_q,
        responses_json=json.dumps(user_answers),
        evaluation_json=json.dumps({"recommendation": recommendation, "correct_count": correct_count}),
        clarity_awarded=clarity_awarded,
        xp_awarded=xp_awarded,
    )
    db.add(attempt)

    profile = db.query(LearnerProfile).filter_by(user_id=user_id).one_or_none()
    if profile:
        profile.xp += xp_awarded
        profile.clarity = min(100, profile.clarity + clarity_awarded)
        if score_pct >= 80:
            profile.clarity_streak += 1

    db.commit()
    db.refresh(attempt)

    return AssessmentAttemptResponse(
        id=attempt.id,
        assessment_id=assessment.id,
        score=score_pct,
        total_questions=total_q,
        clarity_awarded=clarity_awarded,
        xp_awarded=xp_awarded,
        feedback=feedback,
        recommendation=recommendation,
        completed_at=attempt.completed_at,
    )


async def check_and_award_achievements(
    db: Session,
    user_id: int,
    profile: LearnerProfile | None,
    attempt_result: str,
    had_misconception: bool,
) -> None:
    # Ensure standard achievements exist in DB
    achievements_def = [
        ("FIRST_CLARITY", "First Clarity", "Completed your first conceptual exercise", "🌟", 50, 15),
        ("MISCONCEPTION_BREAKER", "Misconception Breaker", "Successfully resolved a learning misconception", "🛠️", 75, 20),
        ("DEEP_THINKER", "Deep Thinker", "Demonstrated high-level reasoning", "🧠", 100, 25),
        ("CONSISTENCY_BUILDER", "Consistency Builder", "Built a 3-day Clarity Streak", "🔥", 100, 30),
    ]

    for code, title, desc, icon, xp, clarity in achievements_def:
        existing = db.query(Achievement).filter_by(code=code).one_or_none()
        if not existing:
            existing = Achievement(code=code, title=title, description=desc, icon=icon, xp_reward=xp, clarity_reward=clarity)
            db.add(existing)
            db.flush()

        # Check unlock condition
        unlocked = db.query(UserAchievement).filter_by(user_id=user_id, achievement_id=existing.id).first()
        if not unlocked:
            should_unlock = False
            if code == "FIRST_CLARITY" and attempt_result == "correct":
                should_unlock = True
            elif code == "MISCONCEPTION_BREAKER" and had_misconception and attempt_result == "correct":
                should_unlock = True
            elif code == "DEEP_THINKER" and profile and profile.xp >= 150:
                should_unlock = True
            elif code == "CONSISTENCY_BUILDER" and profile and profile.clarity_streak >= 3:
                should_unlock = True

            if should_unlock:
                db.add(UserAchievement(user_id=user_id, achievement_id=existing.id))
                if profile:
                    profile.xp += existing.xp_reward
                    profile.clarity = min(100, profile.clarity + existing.clarity_reward)
