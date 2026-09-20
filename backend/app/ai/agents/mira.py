from app.ai.router import build_provider_router
from app.schemas.learning import ActivityPlan


class MiraTeachingAgent:
    """MIRA — Teaching Agent ('The Patient Mentor')
    Purpose: Explain concepts simply and adaptively.
    Responsibilities: Concept explanation, examples, analogies, visual explanations, guided learning, hints.
    """

    async def generate_explanation(self, concept: str, objective: str, learner_state: str, interests: str | None = None) -> ActivityPlan:
        prompt = f"""You are MIRA, the Patient Mentor teaching agent in CLARIO.
Your task is to craft an engaging, intuitive concept explanation for a learner.

Concept: {concept}
Objective: {objective}
Learner State: {learner_state}
Learner Interests/Context: {interests or 'General examples'}

GUIDELINES:
1. Use a simple, encouraging tone ("Let's make this click").
2. Include a relatable analogy or concrete worked example using the learner's interests if applicable.
3. Break complex ideas into easy visual or logical mental models.
4. End with a reflective check question for the learner.

Return JSON matching ActivityPlan schema:
{{
  "activity_type": "explanation",
  "prompt": "Full explanation text with clear markdown formatting and check question",
  "expected_response": "Key points that demonstrate understanding"
}}
"""
        router = build_provider_router()
        return await router.generate_structured(prompt, ActivityPlan)

    async def generate_misconception_repair(self, concept: str, misconception_text: str, learner_state: str) -> ActivityPlan:
        prompt = f"""You are MIRA, repairing a learner misconception in CLARIO.

Concept: {concept}
Detected Misconception: {misconception_text}
Learner Context: {learner_state}

GUIDELINES:
1. Validate the learner's effort: "Your idea is close, but one key part is missing."
2. Explain specifically WHY the misconception happens and clarify the core truth.
3. Provide a clear hint or mini exercise to help them self-correct.

Return JSON matching ActivityPlan schema:
{{
  "activity_type": "misconception_repair",
  "prompt": "Warm misconception explanation and target hint question",
  "expected_response": "The correct understanding after repair"
}}
"""
        router = build_provider_router()
        return await router.generate_structured(prompt, ActivityPlan)
