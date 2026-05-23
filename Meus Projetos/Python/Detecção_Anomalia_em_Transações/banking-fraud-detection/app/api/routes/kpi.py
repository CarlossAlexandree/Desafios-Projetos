from fastapi import APIRouter
import pandas as pd
from app.utils.metrics import fraud_rate, high_risk_transactions

router = APIRouter()

@router.get("/kpi")
def get_kpi():
    # Carregar o dataset original
    df = pd.read_csv("app/data/raw/banking_transactions.csv")

    # Calcular métricas
    return {
        "fraud_rate": round(fraud_rate(df), 3),
        "high_risk_transactions": high_risk_transactions(df),
        "total_transactions": len(df)
    }
