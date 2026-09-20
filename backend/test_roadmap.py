import asyncio
import sys
from app.db.session import get_db, engine, SessionLocal
from app.models.learner import LearningSession, Roadmap, RoadmapNode, User
from app.schemas.learning import RoadmapPlan
from app.orchestrator.workflow import run_roadmap_workflow
from app.ai.router import build_provider_router

async def test():
    # 1. Test DB connection
    print("=== DB Connection ===")
    try:
        with engine.connect() as conn:
            result = conn.execute(__import__('sqlalchemy').text("SELECT 1"))
            print("DB OK:", result.fetchone())
    except Exception as e:
        print("DB FAIL:", e)
        return

    # 2. Test AI provider
    print("\n=== AI Provider Test ===")
    try:
        router = build_provider_router()
        plan = await router.generate_structured(
            "Task: Learn Python. Goal: Write a simple program. Learner state: Beginner. Interests: Games.",
            RoadmapPlan
        )
        print("AI OK. Plan:", plan.title, len(plan.nodes), "nodes")
    except Exception as e:
        print("AI FAIL:", type(e).__name__, str(e)[:200])

    # 3. Test full workflow
    print("\n=== Full Roadmap Workflow ===")
    try:
        with next(get_db()) as db:
            # Find a session
            session = db.query(LearningSession).filter_by(status="active").first()
            if not session:
                print("No active session found. Create one first via POST /sessions")
                return
            
            print(f"Session: {session.id}, task: {session.task[:50]}...")
            roadmap = await generate_roadmap(db, session)
            print(f"Roadmap created: {roadmap.id}, title: {roadmap.title}, nodes: {len(roadmap.nodes)}")
    except Exception as e:
        print("Workflow FAIL:", type(e).__name__, str(e)[:300])

from app.learning.service import generate_roadmap

asyncio.run(test())
