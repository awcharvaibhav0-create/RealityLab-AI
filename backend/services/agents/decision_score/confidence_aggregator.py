from typing import List
from .models import ScenarioOutput
from .confidence import ConfidenceScore


class ConfidenceAggregator:
    """Aggregates confidence scores across multiple scenarios."""

    def aggregate(self, scenarios: List[ScenarioOutput]) -> ConfidenceScore:
        if not scenarios:
            return ConfidenceScore(value=0.0, factors={})

        avg_conf = sum(s.confidence for s in scenarios) / len(scenarios)
        return ConfidenceScore(value=avg_conf, factors={"sample_size": len(scenarios)})
