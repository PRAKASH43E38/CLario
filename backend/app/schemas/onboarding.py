from pydantic import BaseModel, Field, field_validator


class ProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    age_range: str | None = Field(default=None, max_length=32)
    education_level: str | None = Field(default=None, max_length=128)
    domain: str | None = Field(default=None, max_length=255)
    prior_learning: str | None = Field(default=None, max_length=4000)


class MindsetAnswer(BaseModel):
    question_number: int = Field(ge=1, le=5)
    answer: str

    @field_validator("answer")
    @classmethod
    def valid_choice(cls, value: str) -> str:
        choice = value.strip().upper()
        if choice not in {"A", "B", "C", "D"}:
            raise ValueError("answer must be A, B, C, or D")
        return choice


class MindsetSubmission(BaseModel):
    answers: list[MindsetAnswer]

    @field_validator("answers")
    @classmethod
    def exactly_five_questions(cls, value: list[MindsetAnswer]) -> list[MindsetAnswer]:
        if len(value) != 5 or {item.question_number for item in value} != {1, 2, 3, 4, 5}:
            raise ValueError("exactly one answer for each of the five questions is required")
        return value

