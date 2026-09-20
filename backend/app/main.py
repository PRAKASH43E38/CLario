from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.session import create_tables


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield



app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret, https_only=settings.app_env == "production", same_site="lax")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"name": "CLARIO API", "status": "ok"}
