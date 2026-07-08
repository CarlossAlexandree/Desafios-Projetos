"""Orquestra a geração do modelo de ameaças: prompt -> IA -> parsing -> validação."""
import json
import logging
import re

from app.core.exceptions import AIResponseParsingError
from app.models.schemas import ThreatModelResponse
from app.services.prompt_builder import SYSTEM_PROMPT, build_user_prompt
from app.services.providers.base import AIVisionProvider

logger = logging.getLogger(__name__)

# Fallback: caso o modelo insista em envolver o JSON em ```json ... ```
_JSON_BLOCK_RE = re.compile(r"```(?:json)?\s*(\{.*\})\s*```", re.DOTALL)


def _extract_json(raw_text: str) -> dict:
    """Extrai JSON da resposta da IA, tolerando cercas de markdown residuais."""
    text = raw_text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = _JSON_BLOCK_RE.search(text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Última tentativa: pegar do primeiro '{' ao último '}'
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass

    raise AIResponseParsingError(
        "Não foi possível interpretar a resposta da IA como JSON válido."
    )


async def analyze_architecture(
    provider: AIVisionProvider,
    image_base64: str,
    image_mime_type: str,
    tipo_aplicacao: str,
    autenticacao: str,
    acesso_internet: str,
    dados_sensiveis: str,
    descricao_aplicacao: str,
) -> ThreatModelResponse:
    """Função principal: gera e valida o modelo de ameaças STRIDE."""
    user_prompt = build_user_prompt(
        tipo_aplicacao=tipo_aplicacao,
        autenticacao=autenticacao,
        acesso_internet=acesso_internet,
        dados_sensiveis=dados_sensiveis,
        descricao_aplicacao=descricao_aplicacao,
    )

    logger.info("Enviando imagem + prompt para o provedor '%s'", provider.name)
    raw_response = await provider.generate_threat_model(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        image_base64=image_base64,
        image_mime_type=image_mime_type,
    )

    parsed = _extract_json(raw_response)

    try:
        return ThreatModelResponse(
            threat_model=parsed.get("threat_model", []),
            improvement_suggestions=parsed.get("improvement_suggestions", []),
            summary=parsed.get("summary", ""),
            provider_used=provider.name,
        )
    except Exception as exc:
        logger.error("Resposta da IA não bateu com o schema esperado: %s", parsed)
        raise AIResponseParsingError(
            f"A resposta da IA não corresponde ao formato esperado: {exc}"
        ) from exc
