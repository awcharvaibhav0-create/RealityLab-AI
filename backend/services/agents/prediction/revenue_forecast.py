from datetime import datetime, timedelta
from backend.services.agents.prediction.models import ForecastInput, ForecastOutput
from backend.services.agents.prediction.growth_model import GrowthModel


class RevenueForecaster:
    def forecast(
        self, input_data: ForecastInput, growth_model: GrowthModel
    ) -> ForecastOutput:
        initial_revenue = input_data.historical_data.get("revenue", 0.0)
        values = growth_model.calculate_growth(
            initial_revenue, input_data.time_horizon_months
        )
        time_points = [
            datetime.now() + timedelta(days=30 * i)
            for i in range(1, input_data.time_horizon_months + 1)
        ]
        return ForecastOutput(
            metric_name="Revenue", values=values, time_points=time_points
        )
