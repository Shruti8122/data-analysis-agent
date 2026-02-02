from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    numeric = df.select_dtypes(include="number")

    if numeric.empty:
        return 0

    model = IsolationForest(contamination=0.05, random_state=42)
    preds = model.fit_predict(numeric)

    return int((preds == -1).sum())
