"""
STRIDE Vision Agent — API de análise de ameaças em arquiteturas de software.

Ponto de entrada da aplicação FastAPI. Toda a lógica de negócio vive em
app/services e app/api; este arquivo apenas monta e configura a aplicação.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.logging import setup_logging

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info(
        "Iniciando %s | ambiente=%s | provedor de IA=%s",
        settings.APP_NAME,
        settings.ENVIRONMENT,
        settings.AI_PROVIDER,
    )
    yield
    logger.info("Encerrando %s", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "API que recebe diagramas de arquitetura de software e gera, via IA, "
        "um modelo de ameaças baseado na metodologia STRIDE."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Handler central: toda AppError vira uma resposta JSON consistente."""
    logger.warning("AppError tratada: %s", exc.message)
    return JSONResponse(status_code=exc.status_code, content={"error": exc.message})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Rede de segurança: nunca vazar stack trace bruto para o cliente."""
    logger.exception("Erro não tratado")
    return JSONResponse(
        status_code=500,
        content={"error": "Erro interno no servidor. Tente novamente mais tarde."},
    )


app.include_router(router)
