from typing import List, Dict
from .models import ScenarioOutput, Recommendation
from .decision_score_engine import DecisionScoreEngine
from .score_engine import ScoreEngine
from .validator import Validator
from .normalizer import Normalizer
from .score_normalizer import ScoreNormalizer
from .weight_manager import WeightManager
from .confidence_aggregator import ConfidenceAggregator
from .composite_calculator import CompositeCalculator
from .tie_breaker import TieBreaker
from .ranking_engine import RankingEngine
from .recommendation_builder import RecommendationBuilder


class DecisionScoreAgent:
    def __init__(self, engine=None):
        pass

    def process_scenarios(self, scenarios: List[ScenarioOutput], weights: Dict[str, float]) -> Recommendation:
        """Stub to prevent api_manager from crashing. The real score is calculated dynamically."""
        if not scenarios:
            raise ValueError("Scenarios list cannot be empty")
        
        from .models import StrategyRanking, CompositeScore
        rankings = []
        for s in scenarios:
            comp = CompositeScore(strategy_id=s.strategy_id, total_score=0.0, component_scores={}, overall_confidence=1.0)
            rankings.append(StrategyRanking(strategy_id=s.strategy_id, rank=1, score=comp))
        return Recommendation(recommended_strategy_id="stub", rankings=rankings, rationale="stub")

    def calculate_absolute_score(self, context: Dict) -> int:
        metrics = context.get("metrics", {})
        market_analysis = context.get("market_analysis", {})
        risk_analysis = context.get("risk_analysis", {})
        scenarios = context.get("scenarios", [])
        profile = context.get("profile", {})
        
        # 1. ROI (25%)
        roi = metrics.get("avg_roi", 0.0)
        roi_score = max(0.0, min(100.0, roi))
        
        # 2. Net Profit (20%)
        avg_profit = metrics.get("avg_profit", 0.0)
        avg_revenue = metrics.get("avg_revenue", 1.0)
        profit_margin = (avg_profit / avg_revenue * 100.0) if avg_revenue > 0 else 0.0
        profit_score = max(0.0, min(100.0, profit_margin * 4.0))
        
        # 3. Revenue Growth (15%)
        base_revenue = float(profile.get("expected_revenue", 100000))
        rev_growth = ((avg_revenue / base_revenue) - 1) * 100.0 if base_revenue > 0 else 0.0
        growth_score = max(0.0, min(100.0, rev_growth * 2.5))
        
        # 4. Risk Score (20%) - Inverse
        raw_risk = risk_analysis.get("score", 50)
        risk_score = max(0.0, min(100.0, 100.0 - raw_risk))
        
        # 5. Market Confidence (10%)
        mkt_conf = market_analysis.get("confidence", 50)
        confidence_score = max(0.0, min(100.0, mkt_conf))
        
        # 6. Demand (5%)
        total_demand_adj = sum(float(s.get("adjustments", {}).get("demand", 0)) for s in scenarios)
        avg_demand_adj = total_demand_adj / max(1, len(scenarios))
        demand_score = max(0.0, min(100.0, 50.0 + avg_demand_adj))
        
        # 7. Operational Stability (5%)
        op_stability_score = max(0.0, min(100.0, 85.0 - (len(scenarios) * 2)))
        
        final_score = (
            (roi_score * 0.25) +
            (profit_score * 0.20) +
            (growth_score * 0.15) +
            (risk_score * 0.20) +
            (confidence_score * 0.10) +
            (demand_score * 0.05) +
            (op_stability_score * 0.05)
        )
        
        return int(max(0, min(100, final_score)))
