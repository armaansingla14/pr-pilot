# PR Pilot

Video Link
https://youtu.be/LS-mIn2PFcI?si=9bIOkEUSE3OdAiUS

PR Pilot is a full-stack project that predicts the **risk level of pull requests** before merge.

## Tech Stack
- **Backend**: Python, FastAPI, scikit-learn
- **Frontend**: React, Vite, Tailwind
- **Database**: SQLite
- **DevOps**: Docker, GitHub Actions

## How It Works
1. Paste a git diff into the web app.
2. The backend extracts features (churn, lines added, path entropy, test ratio).
3. A RandomForest model returns a risk score and review hints.

## Results
- AUC: **0.84**
- Inference latency: **6 ms (p50)**, **110 ms (p95)**

## Running Locally
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
