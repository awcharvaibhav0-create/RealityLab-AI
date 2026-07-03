from typing import Dict
from .weights import Weights


class WeightManager:
    """Handles parsing and normalizing weights."""

    def process_weights(self, raw_weights: Dict[str, float]) -> Weights:
        """Normalizes weights so the sum of absolute values is exactly 1.0."""
        total = sum(abs(v) for v in raw_weights.values())
        if total == 0:
            num_weights = len(raw_weights)
            return Weights({k: 1.0 / num_weights for k in raw_weights})

        normalized = {k: v / total for k, v in raw_weights.items()}
        return Weights(normalized)
