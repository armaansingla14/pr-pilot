import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report
import joblib, json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "ml" / "data" / "github_prs_sample.csv"
MODEL_OUT = ROOT / "backend" / "model"
MODEL_OUT.mkdir(parents=True, exist_ok=True)

def main():
    if not DATA.exists():
        raise SystemExit(f"Dataset not found at {DATA}")

    df = pd.read_csv(DATA)
    X = df.drop(columns=["label"])
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)

    y_pred_proba = clf.predict_proba(X_test)[:,1]
    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"AUC: {auc:.3f}")
    print(classification_report(y_test, (y_pred_proba > 0.5).astype(int)))

    joblib.dump(clf, MODEL_OUT / "model.pkl")
    print(f"Saved model to {MODEL_OUT / 'model.pkl'}")

if __name__ == "__main__":
    main()
