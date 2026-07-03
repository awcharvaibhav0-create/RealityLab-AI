from typing import Dict, Any
from .risk_engine import BaseRiskEvaluator
from .models import RiskDetail
from .constants import RiskCategory


class SeasonalRiskEvaluator(BaseRiskEvaluator):
    def evaluate(self, scenario: Dict[str, Any]) -> RiskDetail:
        seasonal = scenario.get("seasonal", {})
        dependency = seasonal.get("dependency", "low")

        score = 30.0
        factors = []
        if dependency == "high":
            score += 40
            factors.append("High seasonal dependency")
        elif dependency == "low":
            factors.append("Low seasonal dependency")

        score = max(0.0, min(100.0, score))
        return RiskDetail(
            category=RiskCategory.SEASONAL.value,
            score=score,
            level=self._determine_level(score).name.title(),
            reason=", ".join(factors) if factors else "No specific factors identified",
        )
