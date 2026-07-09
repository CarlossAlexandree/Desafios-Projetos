"""
llm_provider.py
---------------
Camada de abstração sobre o modelo de linguagem.

Por que isso importa:
- O desafio pede Azure OpenAI, mas nem todo mundo tem crédito pago.
- Este módulo tenta o Azure primeiro (créditos de trial) e, se detectar
  erro de autenticação/cota/limite, cai automaticamente para o Google
  Gemini (camada gratuita), sem quebrar o restante do pipeline.

Conceito de LangChain envolvido: todo `ChatModel` do LangChain segue a
mesma interface `Runnable` (invoke/stream/batch), então trocar de
provedor não exige mudar nenhuma outra parte do código — só a fábrica
abaixo.
"""
from __future__ import annotations

import logging

from src.config import settings

logger = logging.getLogger(__name__)


class LLMProviderError(RuntimeError):
    """Erro levantado quando nenhum provedor de LLM está disponível."""


def _build_azure_llm():
    from langchain_openai import AzureChatOpenAI

    if not (settings.azure_api_key and settings.azure_endpoint and settings.azure_deployment):
        raise LLMProviderError("Credenciais do Azure OpenAI incompletas no .env")

    return AzureChatOpenAI(
        azure_deployment=settings.azure_deployment,
        azure_endpoint=settings.azure_endpoint,
        api_key=settings.azure_api_key,
        api_version=settings.azure_api_version,
        temperature=0,
    )


def _build_gemini_llm():
    from langchain_google_genai import ChatGoogleGenerativeAI

    if not settings.google_api_key:
        raise LLMProviderError("GOOGLE_API_KEY não configurada no .env")

    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_api_key,
        temperature=0,
    )


_BUILDERS = {
    "azure": _build_azure_llm,
    "gemini": _build_gemini_llm,
}


def get_llm(force_provider: str | None = None):
    """
    Retorna uma instância de ChatModel pronta para uso.

    Ordem de tentativa:
      1. `force_provider`, se informado explicitamente.
      2. `settings.llm_provider` (padrão: "azure").
      3. Fallback automático para o provedor restante.

    Levanta LLMProviderError se nenhum provedor funcionar — nesse caso,
    verifique as chaves no .env.
    """
    provider_order = [force_provider] if force_provider else [settings.llm_provider]
    for p in _BUILDERS:
        if p not in provider_order:
            provider_order.append(p)

    last_error: Exception | None = None
    for provider in provider_order:
        builder = _BUILDERS.get(provider)
        if builder is None:
            continue
        try:
            llm = builder()
            # Testa a conexão com uma chamada mínima e barata.
            llm.invoke("ping")
            logger.info("LLM ativo: %s", provider)
            return llm
        except Exception as exc:  # noqa: BLE001 - queremos capturar qualquer falha de provedor
            logger.warning("Provedor '%s' indisponível (%s). Tentando próximo...", provider, exc)
            last_error = exc

    raise LLMProviderError(
        f"Nenhum provedor de LLM disponível. Último erro: {last_error}"
    )
