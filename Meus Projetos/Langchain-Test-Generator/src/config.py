"""
config.py
---------
Carrega e centraliza todas as configurações do projeto a partir de
variáveis de ambiente (.env). Mantém o resto do código desacoplado
de `os.getenv` espalhado por aí — uma boa prática de engenharia.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()  # carrega o arquivo .env se existir


@dataclass(frozen=True)
class Settings:
    # Provedor preferencial
    llm_provider: str = os.getenv("LLM_PROVIDER", "azure").lower()

    # Azure OpenAI
    azure_api_key: str | None = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint: str | None = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    azure_deployment: str | None = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    # Google Gemini (fallback gratuito)
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # Parâmetros do gerador / ciclo TDD
    max_tdd_iterations: int = int(os.getenv("MAX_TDD_ITERATIONS", "3"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
