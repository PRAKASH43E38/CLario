from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.learner import LearnerProfile, MindsetResponse, User
from app.schemas.onboarding import MindsetSubmission, ProfileCreate

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


@router.put("/profile", status_code=204)
def save_profile(payload: ProfileCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> None:
    profile = db.query(LearnerProfile).filter(LearnerProfile.user_id == user.id).one_or_none()
    if profile is None:
        profile = LearnerProfile(user_id=user.id, **payload.model_dump())
        db.add(profile)
    else:
        for key, value in payload.model_dump().items():
            setattr(profile, key, value)
    db.commit()


@router.put("/mindset", status_code=204)
def save_mindset(payload: MindsetSubmission, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> None:
    for answer in payload.answers:
        existing = db.query(MindsetResponse).filter_by(user_id=user.id, question_number=answer.question_number).one_or_none()
        if existing is None:
            db.add(MindsetResponse(user_id=user.id, question_number=answer.question_number, answer=answer.answer))
        else:
            existing.answer = answer.answer
    db.commit()

