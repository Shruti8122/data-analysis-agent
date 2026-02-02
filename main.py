from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import io
import traceback

# Your existing agent imports
from agents.ingestion_agent import load_csv
from agents.scaledown_agent import scaledown
from agents.anomaly_agent import detect_anomalies
from agents.insight_agent import generate_insights

app = FastAPI(title="ScaleDown Data Agent API")

# 1. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        # Read file content
        content = await file.read()
        
        # Wrap bytes in BytesIO
        # Check ingestion_agent.py: ensure it uses pd.read_csv(file_buffer)
        df = load_csv(io.BytesIO(content))

        # Run the Agent Pipeline
        # Add safety checks for each agent call
        meta = scaledown(df)
        anomalies = detect_anomalies(df)
        insights = generate_insights(meta, anomalies)
        
        # 2. MATCHING THE FRONTEND with safer .get() defaults
        return {
            "scale_down_stats": {
                "original_size": f"{len(content) / 1024:.2f} KB",
                "compressed_meta": f"{meta.get('schema_size_kb', 0) if isinstance(meta, dict) else 0:.2f} KB",
                "rows": meta.get("rows", len(df)) if isinstance(meta, dict) else len(df),
                "cols": meta.get("cols", len(df.columns)) if isinstance(meta, dict) else len(df.columns)
            },
            "insights": insights,
            "anomalies": anomalies,
            "recommendation": "Random Forest Regressor (Auto-ML Suggestion)"
        }

    except Exception as e:
        # This catches the 500 error and sends the actual Python error to your console
        error_msg = traceback.format_exc()
        print(error_msg) # This will show up in your Render Logs
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "details": "Look at Render logs for the full Traceback"}
        )

# 3. SERVE FRONTEND (Always keep this at the very bottom)
app.mount("/", StaticFiles(directory="static", html=True), name="static")