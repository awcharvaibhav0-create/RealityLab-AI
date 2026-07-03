from typing import List
from backend.services.agents.prediction.confidence import (
    ConfidenceCalculator,
    ConfidenceMetrics,
)


class ConfidenceEngine:
    def __init__(self, calculator: ConfidenceCalculator):
        self.calculator = calculator

    def generate_intervals(
        self, values: List[float], historical_variance: float
    ) -> ConfidenceMetrics:
        """Generates confidence intervals for predicted values."""
        bounds = self.calculator.calculate_bounds(values, historical_variance)
        score = max(0.0, 1.0 - historical_variance)
        return ConfidenceMetrics(score=score, bounds=bounds)
