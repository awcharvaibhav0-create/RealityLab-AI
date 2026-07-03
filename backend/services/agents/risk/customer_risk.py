from typing import Dict, Any
from .risk_engine import BaseRiskEvaluator
from .models import RiskDetail
from .constants import RiskCategory


class CustomerRiskEvaluator(BaseRiskEvaluator):
    def evaluate(self, scenario: Dict[str, Any]) -> RiskDetail:
        customer = scenario.get("customer", {})
        retention = customer.get("retention_risk", "medium")

        score = 50.0
        factors = []
        if retention == "high":
            score += 25
            factors.append("High customer retention risk")
        elif retention == "low":
            score -= 20
            factors.append("Low customer retention risk")

        score = max(0.0, min(100.0, score))
        return RiskDetail(
            category=RiskCategory.CUSTOMER.value,
            score=score,
            level=self._determine_level(score).name.title(),
            reason=", ".join(factors) if factors else "No specific factors identified",
        )
