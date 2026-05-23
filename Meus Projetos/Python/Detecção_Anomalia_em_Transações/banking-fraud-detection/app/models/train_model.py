import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from app.features.feature_engineering import create_features

def train():
    df = pd.read_csv("app/data/raw/banking_transactions.csv")
    df = create_features(df)

    categorical_cols = ["payment_channel", "authentication_type"]
    encoders = {}

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    X = df.drop(columns=["fraud_flag"])
    y = df["fraud_flag"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200, max_depth=10, random_state=42
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))

    joblib.dump(model, "app/data/models/fraud_model.pkl")
    joblib.dump(encoders, "app/data/models/encoders.pkl")

    print("Modelo e encoders salvos com sucesso")
