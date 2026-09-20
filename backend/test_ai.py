import asyncio
from app.ai.router import build_provider_router
from app.schemas.learning import RoadmapPlan

async def test():
    print("Testing AI providers...")
    router = build_provider_router()
    for i, provider in enumerate(router.providers):
        print(f"\nProvider {i+1}: {provider.name}")
        try:
            plan = await provider.generate_structured(
                "Task: Learn Physics. Goal: Understand Newton's laws. Learner state: Beginner. Interests: Sports.",
                RoadmapPlan
            )
            print(f"  OK - title: {plan.title}, nodes: {len(plan.nodes)}")
        except Exception as e:
            print(f"  FAIL: {type(e).__name__}: {str(e)[:200]}")

asyncio.run(test())
