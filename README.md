# PR Pilot — AI Code Review & Risk Scoring

**PR Pilot** is a production-style, full‑stack ML project that ingests real GitHub pull requests, extracts features from diffs, and predicts **PR risk** (likelihood of introducing bugs/maintenance pain). It also generates **review hints** (LLM-backed, optional) and a **dashboard** engineers can actually use.

This is designed to impress engineering teams:
- Real-world data (your own GitHub repos via token/webhooks)
- End-to-end ML (data collection → training → serving)
- Full stack (FastAPI API + React/Tailwind frontend)
- Infra basics (Docker Compose, CI on GitHub Actions)
- Clean repo structure and tests

---

## Quick Start

### 1) Prereqs
- Python 3.10+
- Node 18+
- (Optional) Docker Desktop
- A GitHub personal access token if you want to ingest real PRs

### 2) Create your `.env`
Copy the example:
```bash
cp .env.example .env
```
Set:
- `GITHUB_TOKEN` (classic or fine-grained; needs `repo` read)
- `OPENAI_API_KEY` (optional; if set, LLM suggestions are enabled)

### 3) Train a tiny model (works out of the box)
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
python ml/train.py
```

### 4) Run the stack (dev, without Docker)
In one shell (API):
```bash
uvicorn backend.app.main:app --reload --port 8000
```
In another shell (web):
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

### 5) Run with Docker
```bash
docker compose up --build
```
API at http://localhost:8000, Web at http://localhost:5173

---

## What it does

- **Risk scoring** of a PR/diff using features like:
  - Files changed, churn (additions/deletions), test code ratio, entropy of touched paths
  - Simple complexity signals (e.g., `if|for|while|catch` density), secret/credential patterns
- **LLM-backed review** *(optional)*: If `OPENAI_API_KEY` is set, backend asks an LLM for concrete review hints focused on the diff.
- **Data ingestion from GitHub**: `ml/ingest_github.py` fetches PR metadata + diffs for chosen repos.
- **Training**: `ml/train.py` builds a baseline model (RandomForest) and exports `backend/model/model.pkl`.
- **Serving**: FastAPI endpoint `/analyze` accepts raw diff text or a GitHub PR URL. Returns risk score,
  top features, and review hints.
- **Frontend**: React + Vite + Tailwind app with a dashboard, a playground to paste diffs, and a history view.

---

## Repo Structure

```
pr-pilot/
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app & routes
│   │   ├── feature_engineering.py# Diff → feature vector
│   │   ├── schemas.py            # Pydantic models
│   │   ├── store.py              # SQLite persistence via SQLAlchemy
│   │   ├── llm.py                # Optional LLM suggestions
│   │   └── __init__.py
│   ├── model/
│   │   └── model.pkl             # produced by training (after you run ml/train.py)
│   └── requirements.txt
├── ml/
│   ├── train.py                  # trains RandomForest on dataset
│   ├── ingest_github.py          # scripts to pull PRs/diffs
│   └── data/github_prs_sample.csv# tiny synthetic dataset to start
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── pages/Playground.jsx
│       ├── pages/Dashboard.jsx
│       └── components/AnalysisCard.jsx
├── docker-compose.yml
├── .github/workflows/ci.yml
├── .env.example
└── README.md
```

---

## Ship to GitHub

```bash
git init
git add .
git commit -m "feat: initial PR Pilot stack"
git branch -M main
git remote add origin YOUR_REPO_URL
git push -u origin main
```

---

## Roadmap Ideas

- Webhook for real-time PR updates
- Repo-wide embeddings + semantic search of past PRs
- Language-aware complexity metrics (Tree-sitter)
- Better labels: detect “risky” via reverts/issues referencing PR number
- Model monitoring (drift, performance) and MLflow tracking
