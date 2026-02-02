from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from agents.ingestion_agent import load_csv
from agents.scaledown_agent import scaledown
from agents.anomaly_agent import detect_anomalies
from agents.insight_agent import generate_insights
from agents.profiling_agent import generate_profile
from agents.visualization_agent import generate_plots
from agents.automl_agent import run_automl
import os

app = FastAPI(title="ScaleDown Data Science Agent")

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    df = load_csv(content)

    generate_profile(df)

    meta = scaledown(df)
    anomaly_count = detect_anomalies(df)
    insights = generate_insights(meta, anomaly_count)
    model_rec = run_automl(df)

    plots = generate_plots(df)
    os.makedirs("reports", exist_ok=True)

    for i, fig in enumerate(plots):
        fig.savefig(f"reports/plot_{i+1}.png")
        fig.clf()

    return {
        "scale_down_stats": meta,
        "insights": insights,
        "anomalies": [f"{anomaly_count} anomalous records detected"],
        "recommendation": model_rec,
        "report": "/download_report"
    }

@app.get("/download_report")
def download_report():
    return FileResponse("reports/report.html", media_type="text/html")
