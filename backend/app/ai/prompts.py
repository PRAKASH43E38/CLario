from app.models.learner import LearningSession


def roadmap_prompt(session: LearningSession) -> str:
    return f"""You are CLARIO's Main Orchestrator. Create a personalized learning roadmap.
Return JSON matching the RoadmapPlan schema: title, objective, and 1-12 nodes.
Each node must use activity_type explanation, reasoning, application, assessment, or practice;
difficulty easy, medium, or hard; and estimated_minutes between 3 and 90.
Prioritize conceptual clarity, not course completion. Do not assume the learner is a fixed learning type.

Task: {session.task}
Goal: {session.goal}
Learner state: {session.learner_state}
Interests and context: {session.interests}
"""


def activity_prompt(concept: str, objective: str, activity_type: str, learner_state: str) -> str:
    return f"""Create one interactive CLARIO learning activity as JSON matching ActivityPlan.
The activity must require the learner to think or act, not merely recall a definition.
Use the requested type and give a supportive, concise prompt. Do not reveal the answer in the prompt.
Concept: {concept}
Objective: {objective}
Activity type: {activity_type}
Learner state: {learner_state}
"""


def evaluation_prompt(concept: str, objective: str, activity_prompt_text: str, expected_response: str | None, learner_response: str) -> str:
    return f"""Evaluate a learner response as CLARIO's Elara evaluator. Return JSON matching EvaluationPlan.
Use multiple evidence signals in the response: understanding, reasoning, application, and misconception recovery.
Never say only 'wrong'. Feedback must identify the missing idea and give a useful next step.
Concept: {concept}
Objective: {objective}
Activity: {activity_prompt_text}
Expected response guidance: {expected_response or 'Use the objective and concept to evaluate.'}
Learner response: {learner_response}
"""
