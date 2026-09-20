from app.ai.router import build_provider_router
from app.schemas.learning import ZaynAssessmentPlan


class ZaynQuizAgent:
    """ZAYN — Quiz / Assessment Agent ('The Fair Examiner')
    Purpose: Structured assessment.
    Generates EXACTLY 5 questions per assessment with locked timing rules:
      - Easy: 30 seconds per question
      - Medium: 60 seconds per question
      - Hard: 90 seconds per question
    """

    async def generate_assessment(self, concept: str, objective: str, difficulty: str = "medium") -> ZaynAssessmentPlan:
        time_limits = {"easy": 30, "medium": 60, "hard": 90}
        time_limit = time_limits.get(difficulty.lower(), 60)

        prompt = f"""You are ZAYN, the Fair Examiner assessment agent in CLARIO.
Your task is to generate a structured 5-question assessment.

Concept: {concept}
Objective: {objective}
Difficulty: {difficulty}

REQUIREMENTS:
1. Generate EXACTLY 5 questions. No more, no less.
2. Mix of conceptual understanding, reasoning, and practical application questions.
3. For MCQ questions, provide EXACTLY 4 distinct option choices.
4. Set time_limit_per_question to {time_limit}.

Return JSON matching ZaynAssessmentPlan schema:
{{
  "title": "Assessment: {concept}",
  "difficulty": "{difficulty}",
  "time_limit_per_question": {time_limit},
  "questions": [
    {{
      "position": 1,
      "question_text": "Question 1 text...",
      "question_type": "mcq",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "Why Option A is correct..."
    }},
    ... total 5 questions
  ]
}}
"""
        router = build_provider_router()
        return await router.generate_structured(prompt, ZaynAssessmentPlan)
