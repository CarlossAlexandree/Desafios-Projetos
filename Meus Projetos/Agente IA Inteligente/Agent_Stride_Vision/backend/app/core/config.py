"""
Configurações centralizadas da aplicação.

Usa pydantic-settings para carregar e validar variáveis de ambiente uma
única vez na inicialização, evitando `os.getenv` espalhado pelo código
(anti-pattern comum em protótipos de curso).
"""
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Geral ---
    APP_NAME: str = "STRIDE Vision Agent"
    ENVIRONMENT: Literal["development", "production"] = "development"
    LOG_LEVEL: str = "INFO"

    # --- CORS ---
    # Em produção, restrinja para o(s) domínio(s) real(is) do seu frontend.
    ALLOWED_ORIGINS: str = "http://localhost:8080,http://127.0.0.1:8080"

    # --- Provedor de IA (abstrai Azure OpenAI / Gemini / Groq / Ollama) ---
    AI_PROVIDER: Literal["gemini", "groq", "azure_openai", "ollama"] = "gemini"

    # Google Gemini (provedor padrão gratuito)
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # Groq (alternativa gratuita e muito rápida)
    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "llama-3.2-11b-vision-preview"

    # Azure OpenAI (mantido para compatibilidade com o material do curso)
    AZURE_OPENAI_API_KEY: str | None = None
    AZURE_OPENAI_ENDPOINT: str | None = None
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    AZURE_OPENAI_DEPLOYMENT_NAME: str | None = None

    # Ollama (100% local e gratuito, sem chave de API)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2-vision"

    # --- Limites de upload ---
    MAX_IMAGE_SIZE_MB: int = 8
    ALLOWED_IMAGE_TYPES: str = "image/png,image/jpeg,image/webp"

    # --- Rate limiting simples ---
    RATE_LIMIT_PER_MINUTE: int = 10

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

    @property
    def allowed_image_types_list(self) -> list[str]:
        return [t.strip() for t in self.ALLOWED_IMAGE_TYPES.split(",") if t.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cache simples: lê o .env apenas uma vez por processo."""
    return Settings()
