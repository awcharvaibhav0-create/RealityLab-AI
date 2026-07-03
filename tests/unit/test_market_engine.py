from backend.services.agents.market.market_engine import MarketEngine


def test_market_engine_analyze():
    engine = MarketEngine()
    result = engine.analyze(
        {
            "business_type": "base_retail_business",
            "location": {"base_footfall": 100},
            "competition": {"count": 2},
        }
    )
    assert result.confidence in ["Medium", "High"]
    # Base score = 50
    # Location footfall (100) -> +10 = 60
    # Competition penalty (2) -> -4 = 56
    assert result.market_score == 56.0
