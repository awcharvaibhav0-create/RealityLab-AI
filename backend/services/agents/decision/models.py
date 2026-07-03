from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class DecisionContext(BaseModel):
    analysis_data: Dict[str, Any] = Field(description="Deterministic analysis data")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class RecommendationDecision(BaseModel):
    decision: str
    score: int
    confidence: str
    explainability: List[str]
    executive_recommendations: List[str]


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
