"""Modelos Pydantic — contrato formal de entrada e saída da API."""
from enum import Enum

from pydantic import BaseModel, Field


class TipoAplicacao(str, Enum):
    web = "Web Application"
    mobile = "Mobile Application"
    api = "API / Microsserviço"
    desktop = "Desktop Application"
    cloud_native = "Cloud Native / Serverless"
    outro = "Outro"


class NivelAcesso(str, Enum):
    publico = "Público (exposto à internet)"
    interno = "Interno (rede privada / VPN)"
    hibrido = "Híbrido"


class ThreatItem(BaseModel):
    """Uma ameaça individual dentro de uma categoria STRIDE."""

    threat_type: str = Field(..., description="Uma das 6 categorias STRIDE")
    scenario: str = Field(..., description="Cenário plausível de exploração")
    potential_impact: str = Field(..., description="Impacto potencial no negócio/sistema")
    affected_component: str | None = Field(
        default=None, description="Componente da arquitetura afetado, se identificável"
    )
    severity: str | None = Field(
        default=None, description="Severidade estimada: Baixa, Média, Alta ou Crítica"
    )


class ThreatModelResponse(BaseModel):
    """Resposta completa retornada pela API ao frontend."""

    threat_model: list[ThreatItem] = Field(default_factory=list)
    improvement_suggestions: list[str] = Field(default_factory=list)
    summary: str = Field(default="", description="Resumo executivo da análise")
    provider_used: str = Field(..., description="Provedor de IA que gerou a análise")


class HealthResponse(BaseModel):
    status: str
    environment: str
    ai_provider: str
