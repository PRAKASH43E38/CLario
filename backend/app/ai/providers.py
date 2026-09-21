import json
from abc import ABC, abstractmethod
from typing import Any

import httpx


class LLMProvider(ABC):
    name: str

    @abstractmethod
    async def generate_structured(self, prompt: str, schema: type[Any]) -> Any:
        raise NotImplementedError


def _decode_json(text: str, schema: type[Any]) -> Any:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    try:
        return schema.model_validate_json(cleaned)
    except Exception:
        return schema.model_validate(json.loads(cleaned))


class GeminiProvider(LLMProvider):
    name = "gemini"

    def __init__(self, api_key: str, model: str = "gemini-flash-latest") -> None:
        self.api_key = api_key
        self.model = model

    async def generate_structured(self, prompt: str, schema: type[Any]) -> Any:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"},
        }
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(url, params={"key": self.api_key}, json=payload)
            response.raise_for_status()
            body = response.json()
        text = body["candidates"][0]["content"]["parts"][0]["text"]
        return _decode_json(text, schema)


class OpenAICompatibleProvider(LLMProvider):
    def __init__(self, name: str, api_key: str, base_url: str, model: str) -> None:
        self.name, self.api_key, self.base_url, self.model = name, api_key, base_url.rstrip("/"), model

    async def generate_structured(self, prompt: str, schema: type[Any]) -> Any:
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": "Return only valid JSON matching the requested structure."}, {"role": "user", "content": prompt}],
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(f"{self.base_url}/chat/completions", headers={"Authorization": f"Bearer {self.api_key}"}, json=payload)
            response.raise_for_status()
            body = response.json()
        return _decode_json(body["choices"][0]["message"]["content"], schema)


class LocalFallbackProvider(LLMProvider):
    name = "local_fallback"

    async def generate_structured(self, prompt: str, schema: type[Any]) -> Any:
        schema_name = getattr(schema, "__name__", "")
        if schema_name == "RoadmapPlan":
            return schema.model_validate({
                "title": "Personalized Learning Journey",
                "objective": "Achieve conceptual clarity step by step",
                "nodes": [
                    {
                        "concept": "Foundational Principles",
                        "objective": "Understand basic terms, analogies, and intuition",
                        "activity_type": "explanation",
                        "difficulty": "easy",
                        "estimated_minutes": 10,
                    },
                    {
                        "concept": "Socratic Reasoning & Logic",
                        "objective": "Identify relationships, predict outcomes, and connect ideas",
                        "activity_type": "reasoning",
                        "difficulty": "medium",
                        "estimated_minutes": 15,
                    },
                    {
                        "concept": "Practical Execution & Problem Solving",
                        "objective": "Apply concept to realistic real-world scenarios",
                        "activity_type": "application",
                        "difficulty": "hard",
                        "estimated_minutes": 20,
                    },
                ],
            })
        elif schema_name == "ActivityPlan":
            return schema.model_validate({
                "activity_type": "explanation",
                "prompt": "Explain the concept using a relatable everyday analogy and ask a quick checkpoint question.",
                "expected_response": "Clear explanation connecting the analogy with core principles.",
                "options": ["Option A", "Option B", "Option C", "Option D"],
            })
        elif schema_name == "EvaluationPlan":
            return schema.model_validate({
                "result": "correct",
                "score": 90,
                "feedback": "Great understanding! Your explanation captures the core principles accurately.",
                "misconception": None,
                "recommendation": "progress",
                "clarity_awarded": 20,
                "xp_awarded": 25,
                "confidence_level": "high",
            })
        elif schema_name == "ZaynAssessmentPlan":
            return schema.model_validate({
                "title": "Conceptual Clarity Assessment",
                "difficulty": "medium",
                "time_limit_per_question": 60,
                "questions": [
                    {
                        "position": i,
                        "question_text": f"Question {i}: What is the primary conceptual principle?",
                        "question_type": "mcq",
                        "options": ["A) Principle 1", "B) Principle 2", "C) Principle 3", "D) Principle 4"],
                        "correct_answer": "A) Principle 1",
                        "explanation": "Principle 1 directly addresses the core concept.",
                    }
                    for i in range(1, 6)
                ],
            })
        raise ValueError(f"No fallback generator for schema {schema_name}")


class ProviderRouter:
    """Tries providers in the locked CLARIO order."""

    def __init__(self, providers: list[LLMProvider]) -> None:
        self.providers = providers

    async def generate_structured(self, prompt: str, schema: type[Any]) -> Any:
        last_error: Exception | None = None
        for provider in self.providers:
            try:
                return await provider.generate_structured(prompt, schema)
            except Exception as exc:
                last_error = exc
        
        raise RuntimeError(f"All AI providers failed. Last error: {last_error}")


