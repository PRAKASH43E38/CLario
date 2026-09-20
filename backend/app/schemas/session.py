from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SessionCreate(BaseModel):
    task: str = Field(min_length=3, max_length=2000)
    goal: str = Field(min_length=3, max_length=2000)
    learner_state: str = Field(min_length=3, max_length=4000)
    interests: str = Field(min_length=1, max_length=2000)


class SessionResponse(SessionCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: str
    created_at: datetime

