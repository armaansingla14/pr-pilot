from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import json, os

DB_URL = os.environ.get("DB_URL", "sqlite:///pr_pilot.db")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    diff_text = Column(Text)
    risk_score = Column(Float)
    features_json = Column(Text)
    hints_json = Column(Text)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_analysis(rec: dict):
    with SessionLocal() as s:
        a = Analysis(
            diff_text=rec.get("diff_text","")[:10000],
            risk_score=rec.get("risk_score",0.0),
            features_json=json.dumps(rec.get("features",{})),
            hints_json=json.dumps(rec.get("hints",[])),
        )
        s.add(a)
        s.commit()

def list_analyses(limit=50):
    with SessionLocal() as s:
        rows = s.query(Analysis).order_by(Analysis.id.desc()).limit(limit).all()
        return [{
            "id": r.id,
            "risk_score": r.risk_score,
            "features": json.loads(r.features_json),
            "hints": json.loads(r.hints_json),
        } for r in rows]
