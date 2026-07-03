from typing import Dict, Any
from .risk_engine import BaseRiskEvaluator
from .models import RiskDetail
from .constants import RiskCategory


class ExecutionRiskEvaluator(BaseRiskEvaluator):
    def evaluate(self, scenario: Dict[str, Any]) -> RiskDetail:
        execution = scenario.get("execution", {})
        team_experience = execution.get("team_experience", "medium")

        score = 50.0
        factors = []
        if team_experience == "low":
            score += 30
            factors.append("Low team experience increases execution risk")
        elif team_experience == "high":
            score -= 25
            factors.append("High team experience mitigates execution risk")

        score = max(0.0, min(100.0, score))
        return RiskDetail(
            category=RiskCategory.EXECUTION.value,
            score=score,
            level=self._determine_level(score).name.title(),
            reason=", ".join(factors) if factors else "No specific factors identified",
        )
