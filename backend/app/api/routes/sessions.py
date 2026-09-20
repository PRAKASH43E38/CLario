from fastapi import APIRouter

router = APIRouter(tags=["sessions"])

# Session-related routes were consolidated into app.api.routes.learning.
# This module intentionally stays present as a stable import target for the API router.

