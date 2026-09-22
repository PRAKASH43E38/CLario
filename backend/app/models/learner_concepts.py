"""CLARIO learner concept models — per-concept mastery, learning goals, daily goals."""
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class LearnerConcept(Base):
    __tablename__ = "learner_concepts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    topic: Mapped[str] = mapped_column(String(255), index=True)
    concept: Mapped[str] = mapped_column(String(255))
    mastery: Mapped[float] = mapped_column(Float, default=0.0)
    accuracy: Mapped[float] = mapped_column(Float, default=0.0)
    reasoning_score: Mapped[float] = mapped_column(Float, default=0.0)
    application_score: Mapped[float] = mapped_column(Float, default=0.0)
    consistency: Mapped[float] = mapped_column(Float, default=0.0)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    correct_attempts: Mapped[int] = mapped_column(Integer, default=0)
    mistakes: Mapped[int] = mapped_column(Integer, default=0)
    last_reviewed: Mapped[datetime | None] = mapped_column(DateTime)
    next_review: Mapped[datetime | None] = mapped_column(DateTime)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    review_performance: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(32), default="new")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    __table_args__ = (UniqueConstraint("user_id", "topic", "concept", name="uq_learner_concept"),)


class LearningGoal(Base):
    __tablename__ = "learning_goals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    topic: Mapped[str] = mapped_column(String(255))
    goal_description: Mapped[str] = mapped_column(Text)
    current_level: Mapped[str] = mapped_column(String(32), default="beginner")
    motivation: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


class DailyGoal(Base):
    __tablename__ = "daily_goals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    date: Mapped[datetime] = mapped_column(DateTime)
    learn_concept: Mapped[Boolean] = mapped_column(Boolean, default=False)
    practice_questions: Mapped[Boolean] = mapped_column(Boolean, default=False)
    review_weak: Mapped[Boolean] = mapped_column(Boolean, default=False)
    completed: Mapped[Boolean] = mapped_column(Boolean, default=False)
