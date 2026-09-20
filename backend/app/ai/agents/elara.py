from app.ai.router import build_provider_router
from app.schemas.learning import EvaluationPlan


class ElaraEvaluationAgent:
    """ELARA — Evaluation / Conceptual Clarity Agent ('The Calm Analyst')
    Purpose: Evaluate student responses and assessment results across multiple evidence dimensions.
    Outputs conceptual clarity score, misconception detection, feedback, and next action recommendations.
    """

    async def evaluate_response(
        self,
        concept: str,
        objective: str,
        prompt_text: str,
        expected_response: str | None,
        student_response: str,
    ) -> EvaluationPlan:
        prompt = f"""You are ELARA, the Calm Analyst evaluation agent in CLARIO.
Your task is to evaluate a student's answer for evidence of conceptual clarity.

Concept: {concept}
Objective: {objective}
Task Prompt: {prompt_text}
Expected Answer/Key Points: {expected_response or 'Demonstration of underlying core principles'}
Student Response: {student_response}

EVALUATION RULES:
1. Do NOT evaluate based solely on keyword matching. Look for genuine conceptual understanding and reasoning.
2. Result categories:
   - "correct": Clear understanding demonstrated.
   - "needs_support": Fundamental misunderstanding or misconception present.
   - "partial": Partially correct idea but incomplete or slightly flawed logic.
3. If the student made a mistake, detect the SPECIFIC misconception (e.g., "Confusing correlation with causation", "Missing mass acceleration relationship").
4. Recommendation must be one of: "progress", "practice", "revisit", "deepen".
5. Award XP (10-50) and Clarity (5-25). If misconception resolved, award high Clarity (+20).

Return JSON matching EvaluationPlan schema:
{{
  "result": "correct" | "needs_support" | "partial",
  "score": 0 to 100,
  "feedback": "Encouraging, constructive feedback explaining why it's right or what missing concept to think about",
  "misconception": "Specific misconception summary if result is needs_support or partial, else null",
  "recommendation": "progress" | "practice" | "revisit" | "deepen",
  "clarity_awarded": 5 to 25,
  "xp_awarded": 10 to 50,
  "confidence_level": "high"
}}
"""
        router = build_provider_router()
        return await router.generate_structured(prompt, EvaluationPlan)
