from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import AnalyzeRequest, AnalyzeResponse
from .feature_engineering import extract_features, summarize_features
from .llm import review_hints
from .store import init_db, save_analysis, list_analyses
from pathlib import Path
import joblib, os, json

app = FastAPI(title="PR Pilot API", version="0.1.0")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "model.pkl"
_model = None

@app.on_event("startup")
def _load_model():
    global _model
    init_db()
    if MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    else:
        _model = None

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/analyses")
def analyses():
    return list_analyses(limit=50)

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    # Accept either diff_text or a PR URL (URL not fully implemented here)
    if not req.diff_text and not req.pr_url:
        raise HTTPException(status_code=400, detail="Provide diff_text or pr_url")

    diff_text = req.diff_text or f""  # PR URL ingestion would fetch the diff

    feats = extract_features(diff_text)
    feature_vec = [feats[k] for k in sorted(feats.keys())]
    risk_score = 0.42  # default if model missing
    top_features = summarize_features(feats)

    if _model is not None:
        import numpy as np
        X = np.array(feature_vec).reshape(1, -1)
        risk_score = float(_model.predict_proba(X)[0,1])

    hints = review_hints(diff_text, feats)

    rec = {
        "diff_text": diff_text[:5000],
        "risk_score": risk_score,
        "features": feats,
        "hints": hints,
    }
    save_analysis(rec)

    return AnalyzeResponse(
        risk_score=risk_score,
        features=feats,
        top_features=top_features,
        hints=hints,
    )
