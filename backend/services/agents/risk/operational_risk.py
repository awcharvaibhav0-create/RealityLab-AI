from typing import Dict, Any
from .risk_engine import BaseRiskEvaluator
from .models import RiskDetail
from .constants import RiskCategory


class OperationalRiskEvaluator(BaseRiskEvaluator):
    def evaluate(self, scenario: Dict[str, Any]) -> RiskDetail:
        operations = scenario.get("operations", {})
        complexity = operations.get("complexity", "medium")

        score = 50.0
        factors = []
        if complexity == "high":
            score += 35
            factors.append("High operational complexity")
        elif complexity == "low":
            score -= 15
            factors.append("Low operational complexity")

        score = max(0.0, min(100.0, score))
        return RiskDetail(
            category=RiskCategory.OPERATIONAL.value,
            score=score,
            level=self._determine_level(score).name.title(),
            reason=", ".join(factors) if factors else "No specific factors identified",
        )
