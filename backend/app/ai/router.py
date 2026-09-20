from app.ai.providers import (
    GeminiProvider,
    LLMProvider,
    LocalFallbackProvider,
    OpenAICompatibleProvider,
    ProviderRouter,
)
from app.core.config import settings


def build_provider_router() -> ProviderRouter:
    providers: list[LLMProvider] = []
    if settings.gemini_api_key:
        providers.append(GeminiProvider(settings.gemini_api_key))
    if settings.groq_api_key:
        providers.append(OpenAICompatibleProvider("groq", settings.groq_api_key, "https://api.groq.com/openai/v1", "llama-3.3-70b-versatile"))
    if settings.openrouter_api_key:
        providers.append(OpenAICompatibleProvider("openrouter", settings.openrouter_api_key, "https://openrouter.ai/api/v1", "openai/gpt-4o-mini"))
    if settings.mistral_api_key:
        providers.append(OpenAICompatibleProvider("mistral", settings.mistral_api_key, "https://api.mistral.ai/v1", "mistral-small-latest"))

    providers.append(LocalFallbackProvider())
    return ProviderRouter(providers)

