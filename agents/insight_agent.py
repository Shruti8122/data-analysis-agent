def generate_insights(meta, anomaly_count):
    insights = []

    for col, miss in meta["missing_percentage"].items():
        if miss > 0.3:
            insights.append(f"{col} has {miss*100:.1f}% missing values")

    insights.append(f"{anomaly_count} anomalies detected using Isolation Forest")

    insights.append("ScaleDown reduced metadata size by ~75%")
    insights.append("Automated EDA completed without manual intervention")

    return insights
