from datetime import datetime, timezone

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models.learner import LearnerProfile, User
from app.schemas.auth import AuthUserResponse

router = APIRouter(prefix="/auth", tags=["authentication"])
oauth = OAuth()
google_oauth_configured = bool(settings.google_client_id and settings.google_client_secret)

if google_oauth_configured:
    oauth.register(
        name="google",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile", "timeout": 30.0},
    )


class DevLoginInput(BaseModel):
    email: str = "learner@clario.ai"
    display_name: str = "Alex Learner"


@router.get("/google/start")
async def google_start(request: Request):
    if not google_oauth_configured:
        raise HTTPException(status_code=503, detail="Google OAuth is not configured")
    return await oauth.google.authorize_redirect(request, settings.google_redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    if not google_oauth_configured:
        raise HTTPException(status_code=503, detail="Google OAuth is not configured")

    try:
        token = await oauth.google.authorize_access_token(request)
        profile = token.get("userinfo") or await oauth.google.parse_id_token(request, token)
        if not profile or not profile.get("sub") or not profile.get("email"):
            raise HTTPException(status_code=400, detail="Google account information is incomplete")

        user = db.query(User).filter(User.provider == "google", User.provider_subject == profile["sub"]).one_or_none()
        if user is None:
            user = User(
                provider="google",
                provider_subject=profile["sub"],
                email=profile["email"],
                display_name=profile.get("name"),
            )
            db.add(user)
        user.last_login_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)

        request.session.clear()
        request.session["user_id"] = user.id
        destination = "/home" if user.profile else "/profile"
        # Return a small HTML page which confirms the session is active before redirecting
        # This avoids frontend race where the browser navigates away before the session cookie
        # is fully attached and a subsequent /auth/me call returns 401.
        html = f"""
        <!doctype html>
        <html>
          <head>
            <meta charset=\"utf-8\" />
            <title>Signing you in…</title>
            <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />
            <style>body{{font-family:Inter,system-ui,sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;background:#f7fbf4}}.card{{background:#fff;padding:28px;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.06);text-align:center}}</style>
          </head>
          <body>
            <div class=\"card\"> 
              <div style=\"font-size:24px;font-weight:800;color:#163c32;margin-bottom:8px\">Almost there…</div>
              <div style=\"color:#617c72;font-size:14px\">Finishing sign-in and redirecting you to the app.</div>
            </div>
            <script>
              // Poll /api/v1/auth/me (same origin) until it returns 200, then redirect to frontend
              const dest = "{settings.frontend_url}{destination}";
              const attempts = 8;
              const delay = 300;
              let i = 0;
              async function check(){{
                try{{
                  const r = await fetch('/api/v1/auth/me', {{credentials:'include'}});
                  if (r.status === 200){{ window.location.href = dest; return; }}
                }}catch(e){{/* ignore */}}
                i++;
                if (i < attempts) setTimeout(check, delay);
                else window.location.href = dest; // fallback
              }}
              check();
            </script>
          </body>
        </html>
        """
        return HTMLResponse(content=html)

    except Exception as exc:
        print(f"[OAuth Warning] Google OAuth authentication failed: {exc}")
        return RedirectResponse(f"{settings.frontend_url}/signin?error=oauth_timeout")



@router.post("/dev-login")
def dev_login(payload: DevLoginInput, request: Request, db: Session = Depends(get_db)) -> AuthUserResponse:
    if settings.app_env == "production":
        raise HTTPException(status_code=404, detail="Development login is not available in production.")

    user = db.query(User).filter(User.email == payload.email).one_or_none()
    if user is None:
        user = User(
            provider="local",
            provider_subject=f"local_{payload.email}",
            email=payload.email,
            display_name=payload.display_name,
        )
        db.add(user)
        db.flush()

    user.last_login_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)

    request.session.clear()
    request.session["user_id"] = user.id

    return AuthUserResponse(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        onboarding_complete=user.profile is not None,
    )


@router.get("/me", response_model=AuthUserResponse)
def auth_me(user: User = Depends(get_current_user)) -> AuthUserResponse:
    return AuthUserResponse(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        onboarding_complete=user.profile is not None,
    )


@router.post("/logout", status_code=204)
def logout(request: Request) -> None:
    request.session.clear()
