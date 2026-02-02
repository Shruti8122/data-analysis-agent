from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    numeric = df.select_dtypes(include='number')
    model = IsolationForest(contamination=0.05)
    preds = model.fit_predict(numeric)
    return int((preds == -1).sum())