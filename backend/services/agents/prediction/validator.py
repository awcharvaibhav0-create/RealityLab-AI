from backend.services.agents.prediction.models import ForecastInput


class InputValidator:
    def validate(self, data: ForecastInput) -> bool:
        if data.time_horizon_months <= 0:
            raise ValueError("Time horizon must be positive")
        if not data.historical_data:
            raise ValueError("Historical data cannot be empty")
        return True
