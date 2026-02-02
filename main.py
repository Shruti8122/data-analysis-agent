from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import io

# Your existing agent imports
from agents.ingestion_agent import load_csv
from agents.scaledown_agent import scaledown
from agents.anomaly_agent import detect_anomalies
from agents.insight_agent import generate_insights

app = FastAPI(title="ScaleDown Data Agent API")

# 1. FIX: Enable CORS so your browser doesn't block the request
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In a real project, you'd put your Render URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    # Read file content
    content = await file.read()
    
    # Pro-tip: Wrap bytes in BytesIO if your load_csv expects a file-like object
    df = load_csv(io.BytesIO(content))

    # Run the Agent Pipeline
    meta = scaledown(df)
    anomalies = detect_anomalies(df)
    insights = generate_insights(meta, anomalies)
    
    # 2. MATCHING THE FRONTEND: Return keys that the UI expects
    return {
        "scale_down_stats": {
            "original_size": f"{len(content) / 1024:.2f} KB",
            "compressed_meta": f"{meta.get('schema_size_kb', 0):.2f} KB",
            "rows": meta.get("rows"),
            "cols": meta.get("cols")
        },
        "insights": insights,
        "anomalies": anomalies,
        "recommendation": "Random Forest Regressor (Auto-ML Suggestion)" # Placeholder for your model agent
    }

# 3. SERVE FRONTEND: This mounts the 'static' folder to the root URL
# Make sure your index.html is inside a folder named 'static'
app.mount("/", StaticFiles(directory="static", html=True), name="static")