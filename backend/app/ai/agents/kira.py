from app.ai.router import build_provider_router
from app.schemas.learning import ActivityPlan


class KiraApplicationAgent:
    """KIRA — Real-World Application Agent ('The Practical Coach')
    Purpose: Convert conceptual knowledge into practical execution.
    Creates tasks requiring actual action: coding, algorithm design, scenario decisions, or engineering problem solving.
    """

    async def generate_application_task(self, concept: str, objective: str, learner_state: str, interests: str | None = None) -> ActivityPlan:
        prompt = f"""You are KIRA, the Practical Coach application agent in CLARIO.
Your task is to create a realistic execution task for a learner.

Concept: {concept}
Objective: {objective}
Learner Context/Interests: {interests or 'General engineering & practical applications'}

REQUIREMENTS:
1. Ground the problem in a real-world scenario (e.g. system design, coding problem, engineering tradeoff, business simulation).
2. Ask the learner to write code, design an algorithm, or outline a practical solution step by step.
3. Example style: "You are designing a vehicle control module. What happens to acceleration if mass doubles while engine force stays constant? Write the calculation or code snippet."

Return JSON matching ActivityPlan schema:
{{
  "activity_type": "application",
  "prompt": "Scenario introduction followed by explicit practical action task",
  "expected_response": "Correct code, formula, or practical action steps"
}}
"""
        router = build_provider_router()
        return await router.generate_structured(prompt, ActivityPlan)
