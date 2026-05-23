from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import pandas as pd
from app.features.feature_engineering import create_features
from app.utils.metrics import fraud_rate, high_risk_transactions

router = APIRouter()

@router.get("/dashboard/html", response_class=HTMLResponse)
def dashboard_html():
    # Carregar dataset e calcular métricas
    df = pd.read_csv("app/data/raw/banking_transactions.csv")
    df = create_features(df)

    fraud_rate_value = round(fraud_rate(df), 3)
    high_risk_count = high_risk_transactions(df)
    total_transactions = len(df)

    # Página HTML com KPIs + gráficos
    html_content = f"""
    <html>
        <head>
            <title>Fraud Detection Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2c3e50; }}
                .kpi {{ margin-bottom: 20px; }}
                .kpi span {{ font-weight: bold; color: #e74c3c; }}
                img {{ margin-bottom: 30px; border: 1px solid #ccc; }}
            </style>
        </head>
        <body>
            <h1>Fraud Detection Dashboard</h1>

            <div class="kpi">
                <p>Taxa de Fraude: <span>{fraud_rate_value*100:.2f}%</span></p>
                <p>Transações de Alto Risco: <span>{high_risk_count}</span></p>
                <p>Total de Transações: <span>{total_transactions}</span></p>
            </div>

            <h2>Distribuição de Fraudes</h2>
            <img src="/static/dashboard/fraud_distribution.png" width="600">

            <h2>Fraudes por Canal</h2>
            <img src="/static/dashboard/fraud_by_channel.png" width="600">

            <h2>Fraudes por Horário</h2>
            <img src="/static/dashboard/fraud_by_hour.png" width="600">
        </body>
    </html>
    """
    return html_content
