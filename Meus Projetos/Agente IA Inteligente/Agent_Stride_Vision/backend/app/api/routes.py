"""Rotas HTTP da API."""
import logging

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile

from app.core.config import Settings, get_settings
from app.core.rate_limiter import check_rate_limit
from app.models.schemas import (
    HealthResponse,
    NivelAcesso,
    ThreatModelResponse,
    TipoAplicacao,
)
from app.services.image_service import validate_and_encode_image
from app.services.providers.base import AIVisionProvider
from app.services.providers.factory import get_ai_provider
from app.services.threat_analysis_service import analyze_architecture

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Infra"])
async def health_check(settings: Settings = Depends(get_settings)) -> HealthResponse:
    """Endpoint de liveness/readiness — usado por Docker/orquestradores e monitoramento."""
    return HealthResponse(
        status="ok",
        environment=settings.ENVIRONMENT,
        ai_provider=settings.AI_PROVIDER,
    )


@router.post(
    "/api/v1/analisar-arquitetura",
    response_model=ThreatModelResponse,
    tags=["Análise de Ameaças"],
    summary="Analisa uma imagem de arquitetura e retorna um modelo de ameaças STRIDE",
)
async def analisar_arquitetura(
    request: Request,
    imagem: UploadFile = File(..., description="Imagem do diagrama de arquitetura"),
    tipo_aplicacao: TipoAplicacao = Form(...),
    autenticacao: str = Form(..., description="Ex: OAuth2, JWT, Basic Auth, Nenhuma"),
    acesso_internet: NivelAcesso = Form(...),
    dados_sensiveis: str = Form(..., description="Ex: dados pessoais, financeiros, saúde"),
    descricao_aplicacao: str = Form(
        default="", description="Contexto adicional / conteúdo do README"
    ),
    provider: AIVisionProvider = Depends(get_ai_provider),
) -> ThreatModelResponse:
    """
    Endpoint principal do desafio: recebe uma imagem de arquitetura + contexto
    textual, aplica prompt engineering e retorna um modelo de ameaças STRIDE
    estruturado em JSON.
    """
    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(client_ip)

    image_base64, mime_type = await validate_and_encode_image(imagem)

    logger.info(
        "Analisando arquitetura | tipo=%s | ip=%s | provider=%s",
        tipo_aplicacao.value,
        client_ip,
        provider.name,
    )

    return await analyze_architecture(
        provider=provider,
        image_base64=image_base64,
        image_mime_type=mime_type,
        tipo_aplicacao=tipo_aplicacao.value,
        autenticacao=autenticacao,
        acesso_internet=acesso_internet.value,
        dados_sensiveis=dados_sensiveis,
        descricao_aplicacao=descricao_aplicacao,
    )
