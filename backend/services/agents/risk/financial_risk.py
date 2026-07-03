from typing import Dict, Any
from .risk_engine import BaseRiskEvaluator
from .models import RiskDetail
from .constants import RiskCategory


class FinancialRiskEvaluator(BaseRiskEvaluator):
    def evaluate(self, scenario: Dict[str, Any]) -> RiskDetail:
        profile = scenario.get("profile", {})
        adjustments = scenario.get("scenarios", [{}])[0].get("adjustments", {})
        
        investment = profile.get("investment", 0)
        costs = profile.get("operating_costs", 0)
        cost_adj = adjustments.get("cost", 0)
        
        projected_costs = costs * (1 + (cost_adj / 100.0))

        score = 50.0
        factors = []
        
        if investment > 0 and projected_costs > (investment * 0.8):
            score += 30
            factors.append("High capital exposure relative to operating costs")
        elif investment > 0:
            score -= 20
            factors.append("Healthy capital buffer")
        else:
            factors.append("No financial investment data provided")
            
        if cost_adj > 10:
            score += 20
            factors.append("Significant cost increases projected")

        score = max(0.0, min(100.0, score))
        return RiskDetail(
            category=RiskCategory.FINANCIAL.value,
            score=score,
            level=self._determine_level(score).name.title(),
            reason=", ".join(factors) if factors else "No specific factors identified",
        )
