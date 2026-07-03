from typing import List, Dict
from .models import ScenarioOutput


class Validator:
    """Validates the input scenarios and weights."""

    def validate_scenarios(self, scenarios: List[ScenarioOutput]) -> None:
        if not scenarios:
            raise ValueError("Scenarios list cannot be empty")

        first_keys = set(scenarios[0].metrics.keys())
        if not first_keys:
            raise ValueError("Scenarios must contain at least one metric")

        for s in scenarios:
            if set(s.metrics.keys()) != first_keys:
                raise ValueError("All scenarios must have the exact same metric keys")

    def validate_weights(self, weights: Dict[str, float]) -> None:
        if not weights:
            raise ValueError("Weights cannot be empty")
