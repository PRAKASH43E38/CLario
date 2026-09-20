from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CLARIO API"
    app_env: str = "development"
    frontend_url: str = "http://localhost:5173"
    backend_url: str = "http://localhost:8000"
    database_url: str = "mysql+pymysql://clario:clario@localhost:3306/clario"
    session_secret: str = "development-only-change-me"
    auto_create_tables: bool = False
    google_client_id: str | None = None
    google_client_secret: str | None = None
    google_redirect_uri: str = "http://localhost:8000/api/v1/auth/google/callback"
    gemini_api_key: str | None = None
    groq_api_key: str | None = None
    openrouter_api_key: str | None = None
    mistral_api_key: str | None = None
    tavily_api_key: str | None = None
    langsmith_api_key: str | None = None
    langsmith_project: str = "clario"

    # Resolve the backend env file from this module so the API behaves the
    # same whether uvicorn is started from the repository root or backend/.
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
