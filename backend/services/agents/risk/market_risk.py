from typing import Dict, Any
from .risk_engine import BaseRiskEvaluator
from .models import RiskDetail
from .constants import RiskCategory


class MarketRiskEvaluator(BaseRiskEvaluator):
    def evaluate(self, scenario: Dict[str, Any]) -> RiskDetail:
        profile = scenario.get("profile", {})
        adjustments = scenario.get("scenarios", [{}])[0].get("adjustments", {})
        
        revenue = profile.get("expected_revenue", 0)
        price_adj = adjustments.get("price", 0)
        demand_adj = adjustments.get("demand", 0)

        score = 50.0
        factors = []
        
        if price_adj > 15:
            score += 25
            factors.append("High price increases could reduce market share")
        elif price_adj < 0:
            score -= 10
            factors.append("Competitive pricing strategy")
            
        if demand_adj < 0:
            score += 20
            factors.append("Projecting reduced market demand")
        elif demand_adj > 20:
            score += 15
            factors.append("Overly optimistic demand projections")

        score = max(0.0, min(100.0, score))
        return RiskDetail(
            category=RiskCategory.MARKET.value,
            score=score,
            level=self._determine_level(score).name.title(),
            reason=", ".join(factors) if factors else "No specific factors identified",
        )
