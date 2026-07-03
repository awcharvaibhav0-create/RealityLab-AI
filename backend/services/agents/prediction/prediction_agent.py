from typing import Dict, Any, Optional
from backend.services.agents.prediction.models import ForecastInput, Scenario
from backend.services.agents.prediction.validation import validate_forecast_input
from backend.services.agents.prediction.forecast_engine import ForecastEngine
from backend.services.agents.prediction.confidence_engine import ConfidenceEngine
from backend.services.agents.prediction.confidence import ConfidenceCalculator
from backend.services.agents.prediction.scenario_adjustment import ScenarioAdjuster


class PredictionAgent:
    """Agent responsible for forecasting business performance."""

    def __init__(self):
        calculator = ConfidenceCalculator()
        confidence_engine = ConfidenceEngine(calculator)
        scenario_adjuster = ScenarioAdjuster()
        self.engine = ForecastEngine(confidence_engine, scenario_adjuster)

    def predict(
        self, input_data: ForecastInput, scenario: Optional[Scenario] = None
    ) -> Dict[str, Any]:
        """Runs the prediction models based on historical data and assumptions."""
        validate_forecast_input(input_data)

        results = self.engine.run_forecasts(input_data, scenario)

        # SRS requirements
        confidence = "Medium"
        if input_data.historical_data:
            confidence = "High"

        market_share = input_data.assumptions.get("market_share", 0.05)
        revenue_output = results.get("revenue")
        revenue = (
            revenue_output.values[-1]
            if revenue_output and revenue_output.values
            else 0.0
        )

        from .models import PredictionResult

        prediction_res = PredictionResult(
            expected_outcome="High Growth" if revenue > 100000 else "Steady Growth",
            best_case="Accelerated Expansion",
            worst_case="Stagnation",
            confidence=confidence,
            key_drivers=["Location Footfall", "Competitor Pricing"],
            market_share_yr1=market_share,
            revenue_yr1=revenue,
        )

        return {
            "status": "success",
            "time_horizon_months": input_data.time_horizon_months,
            "data": prediction_res.to_dict(),
            "forecasts": results,
        }
