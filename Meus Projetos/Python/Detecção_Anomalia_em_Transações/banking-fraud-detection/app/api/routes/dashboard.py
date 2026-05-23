from fastapi import APIRouter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from app.features.feature_engineering import create_features

router = APIRouter()

# Pasta onde os gráficos serão salvos
DASHBOARD_DIR = "app/data/processed/dashboard"
os.makedirs(DASHBOARD_DIR, exist_ok=True)

@router.get("/dashboard")
def get_dashboard():
    df = pd.read_csv("app/data/raw/banking_transactions.csv")
    df = create_features(df)

    # Gráfico 1: Distribuição de fraudes
    plt.figure(figsize=(6,4))
    sns.countplot(x="fraud_flag", data=df, palette="Set2")
    plt.title("Distribuição de Fraudes")
    plt.savefig(f"{DASHBOARD_DIR}/fraud_distribution.png")
    plt.close()

    # Gráfico 2: Fraudes por canal
    plt.figure(figsize=(6,4))
    sns.countplot(x="payment_channel", hue="fraud_flag", data=df, palette="Set1")
    plt.title("Fraudes por Canal de Pagamento")
    plt.savefig(f"{DASHBOARD_DIR}/fraud_by_channel.png")
    plt.close()

    # Gráfico 3: Fraudes por horário
    plt.figure(figsize=(6,4))
    sns.histplot(df[df["fraud_flag"]==1]["transaction_time_hour"], bins=24, kde=False, color="red")
    plt.title("Fraudes por Horário da Transação")
    plt.savefig(f"{DASHBOARD_DIR}/fraud_by_hour.png")
    plt.close()

    return {
        "message": "Dashboard gerado com sucesso",
        "charts": {
            "fraud_distribution": "/static/dashboard/fraud_distribution.png",
            "fraud_by_channel": "/static/dashboard/fraud_by_channel.png",
            "fraud_by_hour": "/static/dashboard/fraud_by_hour.png"
        }
    }
