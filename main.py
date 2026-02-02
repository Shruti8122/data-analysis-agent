from fastapi import FastAPI, File, UploadFile
from agents.ingestion_agent import load_csv
from agents.scaledown_agent import scaledown
from agents.anomaly_agent import detect_anomalies
from agents.insight_agent import generate_insights

app = FastAPI()

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    df = load_csv(content)

    meta = scaledown(df)
    anomalies = detect_anomalies(df)
    insights = generate_insights(meta, anomalies)

    return {
        "dataset_shape": meta["rows"],
        "insights": insights,
        "anomalies": anomalies
    }
