from typing import Dict, Any
from .schemas import validate_scenario_schema
from .exceptions import RiskValidationError


class RiskValidator:
    @staticmethod
    def validate(scenario: Dict[str, Any]) -> None:
        """Validate scenario structure before risk assessment."""
        if not isinstance(scenario, dict):
            raise RiskValidationError("Scenario must be a dictionary")
        if not validate_scenario_schema(scenario):
            raise RiskValidationError(
                "Scenario fails schema validation (missing id or description)"
            )
