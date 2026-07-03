from typing import Dict


class Weights:
    """Domain model representing a set of normalized weights."""

    def __init__(self, weights: Dict[str, float]):
        self.weights = weights

    def get(self, key: str, default: float = 0.0) -> float:
        return self.weights.get(key, default)

    def all(self) -> Dict[str, float]:
        return self.weights.copy()
