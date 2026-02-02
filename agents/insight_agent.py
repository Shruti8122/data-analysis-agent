def generate_insights(meta, anomaly_count):
    insights = []

    for col, miss in meta["missing_percentage"].items():
        if miss > 0.3:
            insights.append(f"{col} has {miss*100:.1f}% missing values")

    insights.append(f"Detected {anomaly_count} anomalous records")

    return insights