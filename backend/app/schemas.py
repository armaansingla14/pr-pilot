
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    diff_text: str | None = Field(default=None, description="Unified diff text")
    pr_url: str | None = Field(default=None, description="Optional GitHub PR URL")
    language: str | None = None

class AnalyzeResponse(BaseModel):
    risk_score: float
    features: dict[str, float]
    top_features: list[str]
    hints: list[str]
