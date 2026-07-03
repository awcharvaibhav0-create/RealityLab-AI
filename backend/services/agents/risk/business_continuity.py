from typing import Dict, Any
from .risk_engine import BaseRiskEvaluator
from .models import RiskDetail
from .constants import RiskCategory


class BusinessContinuityRiskEvaluator(BaseRiskEvaluator):
    def evaluate(self, scenario: Dict[str, Any]) -> RiskDetail:
        continuity = scenario.get("business_continuity", {})
        readiness = continuity.get("readiness", "medium")

        score = 50.0
        factors = []
        if readiness == "low":
            score += 35
            factors.append("Low business continuity readiness")
        elif readiness == "high":
            score -= 30
            factors.append("High business continuity readiness")

        score = max(0.0, min(100.0, score))
        return RiskDetail(
            category=RiskCategory.BUSINESS_CONTINUITY.value,
            score=score,
            level=self._determine_level(score).name.title(),
            reason=", ".join(factors) if factors else "No specific factors identified",
        )
