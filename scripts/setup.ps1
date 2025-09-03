# Windows PowerShell bootstrap for PR Pilot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
python ml\train.py
# Run API
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn backend.app.main:app --reload --port 8000"
# Run web
Set-Location frontend
npm install
npm run dev
