from typing import List
from .models import ScenarioOutput, NormalizedScore
from .normalizer import Normalizer


class ScoreNormalizer:
    """Normalizes the metrics across all scenarios."""

    def __init__(self, base_normalizer: Normalizer):
        self.base_normalizer = base_normalizer

    def normalize(self, scenarios: List[ScenarioOutput]) -> List[NormalizedScore]:
        if not scenarios:
            return []

        metrics_keys = scenarios[0].metrics.keys()
        min_max = {
            key: {"min": float("inf"), "max": float("-inf")} for key in metrics_keys
        }

        for s in scenarios:
            for k, v in s.metrics.items():
                if v < min_max[k]["min"]:
                    min_max[k]["min"] = v
                if v > min_max[k]["max"]:
                    min_max[k]["max"] = v

        normalized_scores = []
        for s in scenarios:
            norm_metrics = {}
            for k, v in s.metrics.items():
                norm_metrics[k] = self.base_normalizer.min_max_normalize(
                    v, min_max[k]["min"], min_max[k]["max"]
                )

            normalized_scores.append(
                NormalizedScore(
                    scenario_id=s.scenario_id,
                    strategy_id=s.strategy_id,
                    normalized_metrics=norm_metrics,
                    confidence=s.confidence,
                )
            )

        return normalized_scores
