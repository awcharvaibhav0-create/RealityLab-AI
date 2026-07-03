from typing import Dict, Any
from .risk_engine import BaseRiskEvaluator
from .models import RiskDetail
from .constants import RiskCategory


class CompetitionRiskEvaluator(BaseRiskEvaluator):
    def evaluate(self, scenario: Dict[str, Any]) -> RiskDetail:
        competition = scenario.get("competition", {})
        intensity = competition.get("intensity", "medium")

        score = 50.0
        factors = []
        if intensity == "high":
            score += 30
            factors.append("High competition intensity")
        elif intensity == "low":
            score -= 20
            factors.append("Low competition intensity")

        score = max(0.0, min(100.0, score))
        return RiskDetail(
            category=RiskCategory.COMPETITION.value,
            score=score,
            level=self._determine_level(score).name.title(),
            reason=", ".join(factors) if factors else "No specific factors identified",
        )
