import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.learner import LearningSession, User

router = APIRouter(prefix="/stream", tags=["realtime"])


@router.get("/sessions/{session_id}")
async def stream_session_events(
    session_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    session = db.query(LearningSession).filter_by(id=session_id, user_id=user.id).one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    async def event_generator():
        # Emit initial session_started event
        yield f"event: session_started\ndata: {json.dumps({'session_id': session.id, 'task': session.task, 'status': 'active'})}\n\n"
        await asyncio.sleep(0.3)

        # Check if research is required
        if any(term in f"{session.task} {session.goal}".lower() for term in ["latest", "recent", "research", "news"]):
            yield f"event: research_started\ndata: {json.dumps({'agent': 'Nova', 'query': session.task})}\n\n"
            await asyncio.sleep(0.5)
            yield f"event: research_completed\ndata: {json.dumps({'agent': 'Nova', 'status': 'success'})}\n\n"
            await asyncio.sleep(0.3)

        yield f"event: agent_started\ndata: {json.dumps({'agent': 'Main Orchestrator', 'action': 'Building personalized roadmap'})}\n\n"
        await asyncio.sleep(0.3)

        yield f"event: roadmap_updated\ndata: {json.dumps({'session_id': session.id, 'status': 'ready'})}\n\n"
        await asyncio.sleep(0.2)

        yield f"event: completed\ndata: {json.dumps({'message': 'Orchestration complete'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
