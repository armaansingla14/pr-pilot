# 🛫 PR Pilot

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)

**Catch risky pull requests before they hit `main`.** PR Pilot is a full-stack ML app that reads a git diff, scores how likely the change is to cause problems, and hands the reviewer a short, actionable checklist — all in a few milliseconds.

🎥 **Demo:** https://youtu.be/LS-mIn2PFcI

---

## ✨ Why It's Interesting

Code review is where bugs are supposed to get caught, but reviewers have limited attention and big diffs hide risk. PR Pilot quantifies that risk with hand-engineered features and a trained classifier, then focuses the reviewer's eyes where they matter most (missing tests, leaked secrets, sprawling blast radius).

---

## 🧠 How It Works

```
git diff ──▶ Feature Engineering ──▶ RandomForest ──▶ Risk Score (0–1)
                     │                                        │
                     └───────────────▶ Heuristic Review Hints ┘
```

1. **Paste a diff** (or point at a PR) in the web app.
2. The backend extracts a feature vector from the raw diff text — no repo checkout required.
3. A trained **RandomForest** returns a calibrated **risk score**, and a rules layer adds targeted **review hints**.
4. Every analysis is persisted to SQLite so you can browse history.

### Engineered Features
Built in [`backend/app/feature_engineering.py`](backend/app/feature_engineering.py) straight from the diff:

| Feature | Signal it captures |
|---|---|
| `churn`, `lines_added`, `lines_removed`, `net` | Size / magnitude of the change |
| `files_changed` | Breadth of the edit |
| `path_entropy` | Shannon entropy over touched paths — high = wide blast radius |
| `test_ratio` | Share of changes touching `test/` paths |
| `keyword_density` | Density of control-flow keywords (`if/for/while/try…`) as a complexity proxy |
| `secret_hits` | Regex scan for AWS keys, private keys, hardcoded API keys |

### Review Hints
[`backend/app/llm.py`](backend/app/llm.py) turns those features into human advice ("Low test coverage in touched paths", "Potential secret detected", "High churn — consider splitting"). The hook is LLM-ready: drop in an `OPENAI_API_KEY` to swap heuristics for a model-generated review.

---

## 📊 Results

- **AUC:** `0.84`
- **Inference latency:** `6 ms` p50 · `110 ms` p95

Model trained in [`ml/train.py`](ml/train.py) (200-tree RandomForest, stratified split, ROC-AUC + classification report).

---

## 🛠️ Tech Stack

- **Backend:** Python · FastAPI · scikit-learn · joblib
- **Frontend:** React · Vite · Tailwind CSS
- **Storage:** SQLite
- **DevOps:** Docker · docker-compose · GitHub Actions CI

### API
| Method | Route | Purpose |
|---|---|---|
| `POST` | `/analyze` | Score a diff, return risk + features + hints |
| `GET` | `/analyses` | Recent analysis history |
| `GET` | `/health` | Liveness probe |

---

## 🚀 Run Locally

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (in a second terminal)
cd frontend
npm install
npm run dev
```

Or bring the whole stack up with Docker:

```bash
docker-compose up --build
```

### (Re)train the model
```bash
python ml/train.py    # writes backend/model/model.pkl
```

---

## 👤 Author

**Armaan Singla** — Computer Engineering @ Queen's University
[GitHub](https://github.com/armaansingla14)
