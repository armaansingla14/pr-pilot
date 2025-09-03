from pydantic import BaseModel, Field
from typing import Optional, Dict, List

class AnalyzeRequest(BaseModel):
    diff_text: Optional[str] = Field(default=None, description="Unified diff text")
    pr_url: Optional[str] = Field(default=None, description="Optional GitHub PR URL")
    language: Optional[str] = None

class AnalyzeResponse(BaseModel):
    risk_score: float
    features: Dict[str, float]
    top_features: List[str]
    hints: List[str]
