from backend.services.agents.prediction.models import ForecastOutput


class ROIForecaster:
    def forecast(self, profit_out: ForecastOutput, investment: float) -> ForecastOutput:
        if investment <= 0:
            raise ValueError("Investment must be greater than zero for ROI calculation")
        values = [(p / investment) * 100 for p in profit_out.values]
        return ForecastOutput(
            metric_name="ROI", values=values, time_points=profit_out.time_points
        )
