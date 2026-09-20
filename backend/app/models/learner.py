from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String(32), default="google")
    provider_subject: Mapped[str | None] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    display_name: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime)
    profile: Mapped["LearnerProfile | None"] = relationship(back_populates="user", uselist=False)


class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    age_range: Mapped[str | None] = mapped_column(String(32))
    education_level: Mapped[str | None] = mapped_column(String(128))
    domain: Mapped[str | None] = mapped_column(String(255))
    prior_learning: Mapped[str | None] = mapped_column(Text)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    clarity: Mapped[int] = mapped_column(Integer, default=0)
    clarity_streak: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    user: Mapped[User] = relationship(back_populates="profile")


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    task: Mapped[str] = mapped_column(Text)
    goal: Mapped[str] = mapped_column(Text)
    learner_state: Mapped[str] = mapped_column(Text)
    interests: Mapped[str] = mapped_column(Text)
    learner_context: Mapped[str | None] = mapped_column(Text, default=None)
    status: Mapped[str] = mapped_column(String(32), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class MindsetResponse(Base):
    __tablename__ = "mindset_responses"
    __table_args__ = (UniqueConstraint("user_id", "question_number"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    question_number: Mapped[int] = mapped_column(Integer)
    answer: Mapped[str] = mapped_column(String(1))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("learning_sessions.id"), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    objective: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class RoadmapNode(Base):
    __tablename__ = "roadmap_nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    roadmap_id: Mapped[int] = mapped_column(ForeignKey("roadmaps.id"), index=True)
    position: Mapped[int] = mapped_column(Integer)
    concept: Mapped[str] = mapped_column(String(255))
    objective: Mapped[str] = mapped_column(Text)
    activity_type: Mapped[str] = mapped_column(String(64))
    difficulty: Mapped[str] = mapped_column(String(16), default="medium")
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=10)
    status: Mapped[str] = mapped_column(String(32), default="locked")
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class LearningActivity(Base):
    __tablename__ = "learning_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    node_id: Mapped[int] = mapped_column(ForeignKey("roadmap_nodes.id"), index=True)
    activity_type: Mapped[str] = mapped_column(String(64))
    prompt: Mapped[str] = mapped_column(Text)
    expected_response: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class ActivityAttempt(Base):
    __tablename__ = "activity_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("learning_activities.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    response: Mapped[str] = mapped_column(Text)
    result: Mapped[str] = mapped_column(String(32), default="submitted")
    feedback: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class LearningEvidence(Base):
    __tablename__ = "learning_evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("learning_sessions.id"), index=True)
    concept: Mapped[str] = mapped_column(String(255))
    evidence_type: Mapped[str] = mapped_column(String(64))
    score: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Misconception(Base):
    __tablename__ = "misconceptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("learning_sessions.id"), index=True)
    concept: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="detected")  # detected, repairing, resolved
    detected_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime)


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("learning_sessions.id"), index=True)
    roadmap_id: Mapped[int] = mapped_column(ForeignKey("roadmaps.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    difficulty: Mapped[str] = mapped_column(String(16), default="medium")  # easy (30s), medium (60s), hard (90s)
    time_limit_per_question: Mapped[int] = mapped_column(Integer, default=60)
    questions: Mapped[list["AssessmentQuestion"]] = relationship(back_populates="assessment", cascade="all, delete-orphan")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), index=True)
    position: Mapped[int] = mapped_column(Integer)
    question_text: Mapped[str] = mapped_column(Text)
    question_type: Mapped[str] = mapped_column(String(32), default="mcq")  # mcq, reasoning, prediction
    options_json: Mapped[str | None] = mapped_column(Text)  # JSON string of options
    correct_answer: Mapped[str] = mapped_column(Text)
    explanation: Mapped[str | None] = mapped_column(Text)
    assessment: Mapped[Assessment] = relationship(back_populates="questions")


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    score: Mapped[int] = mapped_column(Integer)
    total_questions: Mapped[int] = mapped_column(Integer, default=5)
    responses_json: Mapped[str] = mapped_column(Text)  # JSON string of user answers
    evaluation_json: Mapped[str | None] = mapped_column(Text)  # Elara evaluation
    clarity_awarded: Mapped[int] = mapped_column(Integer, default=0)
    xp_awarded: Mapped[int] = mapped_column(Integer, default=0)
    completed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    icon: Mapped[str] = mapped_column(String(64), default="🏆")
    xp_reward: Mapped[int] = mapped_column(Integer, default=50)
    clarity_reward: Mapped[int] = mapped_column(Integer, default=20)


class UserAchievement(Base):
    __tablename__ = "user_achievements"
    __table_args__ = (UniqueConstraint("user_id", "achievement_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievements.id"), index=True)
    unlocked_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class LearnerInsight(Base):
    __tablename__ = "learner_insights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    insight_text: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(64), default="learning_style")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

