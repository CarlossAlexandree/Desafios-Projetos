import pandas as pd

def fraud_rate(df: pd.DataFrame) -> float:
    """Taxa de fraude sobre o total de transações"""
    return df["fraud_flag"].mean()

def high_risk_transactions(df: pd.DataFrame) -> int:
    """Número de transações com score de risco elevado"""
    return df[df["risk_score"] > 50].shape[0]

