from backend.services.agents.prediction.validator import InputValidator
from backend.services.agents.prediction.models import ForecastInput


def validate_forecast_input(data: ForecastInput) -> bool:
    validator = InputValidator()
    return validator.validate(data)
