"""Factory: escolhe o provedor de IA de acordo com AI_PROVIDER no .env."""
from functools import lru_cache

from app.core.config import get_settings
from app.core.exceptions import AIProviderError
from app.services.providers.azure_openai_provider import AzureOpenAIProvider
from app.services.providers.base import AIVisionProvider
from app.services.providers.gemini_provider import GeminiProvider
from app.services.providers.groq_provider import GroqProvider
from app.services.providers.ollama_provider import OllamaProvider

_PROVIDERS: dict[str, type[AIVisionProvider]] = {
    "gemini": GeminiProvider,
    "groq": GroqProvider,
    "azure_openai": AzureOpenAIProvider,
    "ollama": OllamaProvider,
}


@lru_cache
def get_ai_provider() -> AIVisionProvider:
    """
    Retorna uma instância (cacheada) do provedor configurado.

    Trocar de provedor é apenas mudar AI_PROVIDER no .env — nenhum código
    de rota ou de negócio precisa mudar.
    """
    settings = get_settings()
    provider_cls = _PROVIDERS.get(settings.AI_PROVIDER)

    if provider_cls is None:
        raise AIProviderError(
            f"Provedor '{settings.AI_PROVIDER}' desconhecido. "
            f"Opções válidas: {', '.join(_PROVIDERS)}"
        )

    return provider_cls()
