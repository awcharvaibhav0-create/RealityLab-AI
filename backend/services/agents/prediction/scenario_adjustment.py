from typing import List
from backend.services.agents.prediction.models import Scenario


class ScenarioAdjuster:
    def apply_scenario(
        self, base_values: List[float], scenario: Scenario, metric: str
    ) -> List[float]:
        adjustment_factor = scenario.adjustments.get(metric, 1.0)
        return [v * adjustment_factor for v in base_values]
