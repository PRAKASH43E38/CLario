from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.learning import router as learning_router
from app.api.routes.onboarding import router as onboarding_router
from app.api.routes.sessions import router as sessions_router
from app.api.routes.stream import router as stream_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(onboarding_router)
api_router.include_router(learning_router)
api_router.include_router(sessions_router)
api_router.include_router(stream_router)
