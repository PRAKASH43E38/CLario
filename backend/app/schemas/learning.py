from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RoadmapNodePlan(BaseModel):
    concept: str = Field(min_length=1, max_length=255)
    objective: str = Field(min_length=3, max_length=2000)
    activity_type: str = Field(pattern="^(explanation|reasoning|application|assessment|practice|misconception_repair)$")
    difficulty: str = Field(pattern="^(easy|medium|hard)$")
    estimated_minutes: int = Field(ge=1, le=90)


class RoadmapPlan(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    objective: str = Field(min_length=3, max_length=2000)
    nodes: list[RoadmapNodePlan] = Field(min_length=1, max_length=12)


class RoadmapNodeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    position: int
    concept: str
    objective: str
    activity_type: str
    difficulty: str
    estimated_minutes: int
    status: str
    is_current: bool


class RoadmapResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    title: str
    objective: str
    status: str
    nodes: list[RoadmapNodeResponse]


class ActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    node_id: int
    activity_type: str
    prompt: str
    expected_response: str | None = None
    options: list[str] | None = None


class ActivityPlan(BaseModel):
    activity_type: str = Field(pattern="^(explanation|reasoning|application|assessment|practice|misconception_repair)$")
    prompt: str = Field(min_length=10, max_length=5000)
    expected_response: str | None = Field(default=None, max_length=5000)
    options: list[str] | None = Field(default=None)


class AttemptCreate(BaseModel):
    response: str = Field(min_length=1, max_length=10000)


class AttemptResponse(BaseModel):
    id: int
    activity_id: int
    result: str
    feedback: str
    score: int
    clarity_awarded: int
    xp_awarded: int
    misconception_detected: str | None = None
    new_node_inserted: bool = False
    new_node: RoadmapNodeResponse | None = None
    created_at: datetime


class EvaluationPlan(BaseModel):
    result: str = Field(pattern="^(correct|needs_support|partial)$")
    score: int = Field(ge=0, le=100)
    feedback: str = Field(min_length=10, max_length=5000)
    misconception: str | None = Field(default=None, max_length=1000)
    recommendation: str = Field(pattern="^(progress|practice|revisit|deepen)$")
    clarity_awarded: int = Field(ge=0, le=50)
    xp_awarded: int = Field(ge=0, le=100)
    confidence_level: str = Field(default="high", pattern="^(low|medium|high)$")


# --- ZAYN ASSESSMENT SCHEMAS ---
class ZaynQuestionPlan(BaseModel):
    position: int = Field(ge=1, le=5)
    question_text: str = Field(min_length=5, max_length=2000)
    question_type: str = Field(pattern="^(mcq|reasoning|prediction)$")
    options: list[str] = Field(default_factory=list, description="4 options for MCQ")
    correct_answer: str = Field(min_length=1, max_length=1000)
    explanation: str = Field(min_length=5, max_length=2000)


class ZaynAssessmentPlan(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    difficulty: str = Field(pattern="^(easy|medium|hard)$")
    time_limit_per_question: int = Field(ge=30, le=90)
    questions: list[ZaynQuestionPlan] = Field(min_length=5, max_length=5)


class QuestionResponse(BaseModel):
    id: int
    position: int
    question_text: str
    question_type: str
    options: list[str]
    time_limit: int


class AssessmentResponse(BaseModel):
    id: int
    roadmap_id: int
    title: str
    difficulty: str
    time_limit_per_question: int
    questions: list[QuestionResponse]


class AssessmentAnswerInput(BaseModel):
    question_id: int
    user_answer: str


class AssessmentSubmission(BaseModel):
    answers: list[AssessmentAnswerInput]


class AssessmentAttemptResponse(BaseModel):
    id: int
    assessment_id: int
    score: int
    total_questions: int
    clarity_awarded: int
    xp_awarded: int
    feedback: str
    recommendation: str
    completed_at: datetime


# --- GAMIFICATION, INSIGHTS & USER STATS SCHEMAS ---
class UserStatsResponse(BaseModel):
    xp: int
    clarity: int
    clarity_streak: int
    level: int
    title: str


class AchievementResponse(BaseModel):
    id: int
    code: str
    title: str
    description: str
    icon: str
    xp_reward: int
    clarity_reward: int
    unlocked: bool
    unlocked_at: datetime | None = None


class LearnerInsightResponse(BaseModel):
    id: int
    insight_text: str
    category: str
    created_at: datetime

