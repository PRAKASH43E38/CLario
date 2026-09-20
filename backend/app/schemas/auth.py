from pydantic import BaseModel, ConfigDict


class AuthUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    display_name: str | None
    onboarding_complete: bool

