from typing import Dict, Any
from datetime import datetime
from shared.knowledge.local_knowledge_base import LocalKnowledgeBase

from .models import MarketResult


class MarketEngine:
    def __init__(self, lkb: LocalKnowledgeBase = None):
        self.lkb = lkb or LocalKnowledgeBase()

    def analyze(self, scenario_data: Dict[str, Any]) -> MarketResult:
        result = MarketResult()

        business_type = scenario_data.get("business_type", "base_retail_business")
        location = scenario_data.get("location", {})
        date_str = scenario_data.get("date", datetime.utcnow().isoformat())
        competition = scenario_data.get("competition", {})

        # Load rules
        active_rules = self.lkb.get_active_rules(business_type).active_rules
        market_rules = active_rules.get("market", {})

        dt = (
            datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            if date_str
            else datetime.utcnow()
        )
        result.analysis_date = dt.strftime("%Y-%m-%d")
        result.analysis_time = dt.strftime("%H:%M")

        # Day analysis
        is_weekend = dt.weekday() >= 5
        result.day_type = "Weekend" if is_weekend else "Weekday"

        # Season analysis (simple logic based on month)
        if dt.month in [3, 4, 5]:
            result.season = "Summer"
        elif dt.month in [6, 7, 8, 9]:
            result.season = "Monsoon"
        else:
            result.season = "Winter"

        # Dynamic Market Trend & Demand based on Scenario
        demand_adjustment = scenario_data.get("adjustments", {}).get("demand", 0)
        
        if demand_adjustment > 10:
            result.market_trend = "Accelerating"
            result.demand = "Very High"
        elif demand_adjustment > 0:
            result.market_trend = "Growing"
            result.demand = "High"
        elif demand_adjustment == 0:
            result.market_trend = "Stable"
            result.demand = "Moderate"
        elif demand_adjustment > -10:
            result.market_trend = "Slowing"
            result.demand = "Low"
        else:
            result.market_trend = "Declining"
            result.demand = "Very Low"

        # Competition
        competitor_count = competition.get("count", 0)
        if competitor_count > 5:
            result.competition = "High"
        elif competitor_count > 2:
            result.competition = "Medium"
        else:
            result.competition = "Low"

        score = 50.0  # Base score

        # 1. Location & Footfall
        base_footfall = location.get("base_footfall", 100)
        footfall_multiplier = market_rules.get("footfall_multiplier", 1.0)
        score += (base_footfall / 100) * 10 * footfall_multiplier

        # 2. Competition
        competition_penalty = market_rules.get("competition_penalty", 2.0)
        score -= competitor_count * competition_penalty

        # 3. Seasonality
        seasonality = market_rules.get("seasonality", {})
        season_multiplier = seasonality.get(str(dt.month), 1.0)
        score *= season_multiplier

        # Normalize score between 0 and 100
        result.market_score = max(0.0, min(100.0, score))

        # Confidence
        result.confidence = "High" if scenario_data.get("historical_data") else "Medium"

        # Assumptions
        result.assumptions = {
            "customer_growth": market_rules.get("expected_customer_growth", 0.04),
            "expense_growth": market_rules.get("expected_expense_growth", 0.02),
            "seasonal_adjustment": season_multiplier,
        }

        return result
