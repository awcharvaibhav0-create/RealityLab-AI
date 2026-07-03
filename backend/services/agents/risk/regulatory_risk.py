from typing import Dict, Any
from .risk_engine import BaseRiskEvaluator
from .models import RiskDetail
from .constants import RiskCategory


class RegulatoryRiskEvaluator(BaseRiskEvaluator):
    def evaluate(self, scenario: Dict[str, Any]) -> RiskDetail:
        regulatory = scenario.get("regulatory", {})
        compliance_burden = regulatory.get("compliance_burden", "medium")

        score = 40.0
        factors = []
        if compliance_burden == "high":
            score += 40
            factors.append("High regulatory compliance burden")
        elif compliance_burden == "low":
            score -= 15
            factors.append("Low regulatory compliance burden")

        score = max(0.0, min(100.0, score))
        return RiskDetail(
            category=RiskCategory.REGULATORY.value,
            score=score,
            level=self._determine_level(score).name.title(),
            reason=", ".join(factors) if factors else "No specific factors identified",
        )
