from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from agents.ingestion_agent import load_csv
from agents.scaledown_agent import scaledown
from agents.anomaly_agent import detect_anomalies
from agents.insight_agent import generate_insights
from agents.profiling_agent import generate_profile
from agents.visualization_agent import generate_plots
import os

app = FastAPI(title="AI Data Analysis Agent")

# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to AI Data Analysis Agent. Use POST /analyze to upload CSV."}

# Analyze endpoint
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Step 1: Load CSV
    content = await file.read()
    df = load_csv(content)

    # Step 2: Generate profiling report
    if not os.path.exists("reports"):
        os.makedirs("reports")
    generate_profile(df)

    # Step 3: Scaledown metadata
    meta = scaledown(df)

    # Step 4: Detect anomalies
    anomalies = detect_anomalies(df)

    # Step 5: Generate insights
    insights = generate_insights(meta, anomalies)

    # Step 6: Generate visualizations
    plots = generate_plots(df)
    # Save plots to files
    plot_files = []
    for i, fig in enumerate(plots):
        path = f"reports/plot_{i+1}.png"
        fig.savefig(path)
        plot_files.append(path)
        fig.clf()  # clear figure

    return {
        "dataset_rows": meta["rows"],
        "dataset_columns": meta["columns"],
        "missing_percentage": meta["missing_percentage"],
        "insights": insights,
        "anomalies_detected": anomalies,
        "profiling_report": "reports/report.html",
        "plots": plot_files
    }

# Endpoint to download profiling report
@app.get("/download_report")
def download_report():
    report_path = "reports/report.html"
    if os.path.exists(report_path):
        return FileResponse(report_path, media_type="text/html", filename="report.html")
    return {"error": "Report not found"}