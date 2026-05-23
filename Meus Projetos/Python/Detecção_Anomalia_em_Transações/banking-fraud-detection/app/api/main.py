import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Importar routers
from app.api.routes.predict import router as predict_router
from app.api.routes.kpi import router as kpi_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.dashboard_html import router as dashboard_html_router

# Criar instância do FastAPI
app = FastAPI(title="Fraud Detection API")

# Registrar rotas
app.include_router(predict_router)
app.include_router(kpi_router)
app.include_router(dashboard_router)
app.include_router(dashboard_html_router)

# Servir arquivos estáticos (gráficos)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "..", "data", "processed")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")



