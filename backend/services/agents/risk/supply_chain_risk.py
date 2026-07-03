from typing import Dict, Any
from .risk_engine import BaseRiskEvaluator
from .models import RiskDetail
from .constants import RiskCategory


class SupplyChainRiskEvaluator(BaseRiskEvaluator):
    def evaluate(self, scenario: Dict[str, Any]) -> RiskDetail:
        supply = scenario.get("supply_chain", {})
        stability = supply.get("stability", "medium")

        score = 50.0
        factors = []
        if stability == "low":
            score += 35
            factors.append("Low supply chain stability")
        elif stability == "high":
            score -= 25
            factors.append("High supply chain stability")

        score = max(0.0, min(100.0, score))
        return RiskDetail(
            category=RiskCategory.SUPPLY_CHAIN.value,
            score=score,
            level=self._determine_level(score).name.title(),
            reason=", ".join(factors) if factors else "No specific factors identified",
        )
