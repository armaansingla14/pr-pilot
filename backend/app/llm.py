import os
from typing import List, Dict

def review_hints(diff_text: str, feats: Dict[str, float]) -> List[str]:
    # If OPENAI_API_KEY is present, you could plug in an LLM call here.
    # To keep the template dependency-light, we'll return heuristic hints.
    hints = []
    if feats.get("secret_hits", 0) > 0:
        hints.append("Potential secret detected. Ensure no credentials are committed.")
    if feats.get("test_ratio", 0) < 0.05:
        hints.append("Low test coverage in touched paths. Consider adding/adjusting tests.")
    if feats.get("churn", 0) > 500:
        hints.append("High churn PR. Consider splitting into smaller, focused changes.")
    if feats.get("keyword_density", 0) > 0.2:
        hints.append("Complex control flow detected; assess readability and add comments.")
    if feats.get("path_entropy", 0) > 3.0:
        hints.append("Changes span many areas; validate integration and side effects.")
    if not hints:
        hints.append("Looks reasonable. Focus review on logic changes and edge cases.")
    return hints
