from app.ai.router import build_provider_router
from app.schemas.learning import ActivityPlan


class AyanReasoningAgent:
    """AYAN — Reasoning / Critical Thinking Agent ('The Socratic Challenger')
    Purpose: Develop and evaluate actual reasoning through typed logic, fill-in-the-blanks,
    predicting outputs, explaining missing steps, and Socratic 'what-if' questions.
    """

    async def generate_reasoning_task(self, concept: str, objective: str, learner_state: str) -> ActivityPlan:
        prompt = f"""You are AYAN, the Socratic Challenger reasoning agent in CLARIO.
Your task is to create a critical thinking / reasoning exercise for a learner.

Concept: {concept}
Objective: {objective}
Learner State: {learner_state}

CRITICAL RULES:
1. Do NOT make this a generic multiple choice question.
2. Require the learner to perform active reasoning: e.g., "Why does X happen when Y changes?", "Predict the outcome of this scenario...", "Find and fix the error in this logical statement...", or "Complete the missing step in this solution."
3. Ask the student to explain their thought process step-by-step in their own words.

Return JSON matching ActivityPlan schema:
{{
  "activity_type": "reasoning",
  "prompt": "Clear reasoning problem statement ending with a Socratic prompt asking for typed reasoning",
  "expected_response": "Key logical reasoning steps expected in the student's answer"
}}
"""
        router = build_provider_router()
        return await router.generate_structured(prompt, ActivityPlan)
