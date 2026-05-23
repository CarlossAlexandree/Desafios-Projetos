from fastapi import APIRouter
from pydantic import BaseModel
import joblib
import pandas as pd
from app.features.feature_engineering import create_features

router = APIRouter()

model = joblib.load("app/data/models/fraud_model.pkl")
encoders = joblib.load("app/data/models/encoders.pkl")

class Transaction(BaseModel):
    transaction_amount: float
    login_attempts: int
    device_risk_score: float
    transfer_frequency: float = 0
    anomaly_score: float = 0
    account_age_days: int = 0
    transaction_time_hour: int = 12
    failed_transactions_last_30d: int = 0
    avg_monthly_balance: float = 0
    daily_transaction_count: int = 0
    geo_distance_km: float = 0
    session_duration_minutes: int = 0
    transaction_velocity_score: float = 0
    payment_channel: str = "online"
    authentication_type: str = "password"
    card_present_flag: int = 0
    international_transaction_flag: int = 0
    suspicious_ip_flag: int = 0

@router.post("/predict")
def predict(transaction: Transaction):
    df = pd.DataFrame([transaction.dict()])
    df = create_features(df)

    # aplicar encoders
    for col, le in encoders.items():
        df[col] = le.transform(df[col].astype(str))

    prob = model.predict_proba(df)[0][1]
    prediction = "FRAUD" if prob > 0.5 else "NOT_FRAUD"
    risk_level = "HIGH" if prob > 0.8 else "MEDIUM" if prob > 0.5 else "LOW"

    return {
        "fraud_probability": round(prob, 2),
        "prediction": prediction,
        "risk_level": risk_level
    }
