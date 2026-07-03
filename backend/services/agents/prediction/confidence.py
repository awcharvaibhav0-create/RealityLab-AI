from dataclasses import dataclass
from typing import List, Dict


@dataclass
class ConfidenceMetrics:
    score: float
    bounds: Dict[str, List[float]]


class ConfidenceCalculator:
    def calculate_bounds(
        self, values: List[float], variance: float
    ) -> Dict[str, List[float]]:
        upper_bound = [v * (1 + variance) for v in values]
        lower_bound = [v * (1 - variance) for v in values]
        return {"upper": upper_bound, "lower": lower_bound}
