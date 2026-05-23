import pandas as pd

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Preencher valores nulos
    df.fillna(0, inplace=True)

    df["risk_score"] = (
        df["device_risk_score"] * 0.3 +
        df["anomaly_score"] * 100 * 0.3 +
        df["transaction_velocity_score"] * 0.2 +
        df["suspicious_ip_flag"] * 20 +
        df["international_transaction_flag"] * 10
    )

    df["suspicious_session"] = (
        (df["login_attempts"] > 5) &
        (df["failed_transactions_last_30d"] > 10)
    ).astype(int)

    df["high_value_transaction"] = (
        df["transaction_amount"] > 15000
    ).astype(int)

    df["velocity_risk"] = (
        df["daily_transaction_count"] *
        df["transaction_velocity_score"]
    )

    return df
