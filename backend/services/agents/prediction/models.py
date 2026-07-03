from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class ForecastInput:
    historical_data: Dict[str, float]
    time_horizon_months: int
    assumptions: Dict[str, float] = field(default_factory=dict)


@dataclass
class ForecastOutput:
    metric_name: str
    values: List[float]
    time_points: List[datetime]
    confidence_intervals: Dict[str, List[float]] = field(default_factory=dict)


@dataclass
class Scenario:
    name: str
    adjustments: Dict[str, float]


@dataclass
class PredictionResult:
    expected_outcome: str
    best_case: str
    worst_case: str
    confidence: str
    key_drivers: List[str]
    market_share_yr1: float
    revenue_yr1: float

    def to_dict(self):
        return {
            "expected_outcome": self.expected_outcome,
            "best_case": self.best_case,
            "worst_case": self.worst_case,
            "confidence": self.confidence,
            "key_drivers": self.key_drivers,
            "market_share_yr1": self.market_share_yr1,
            "revenue_yr1": self.revenue_yr1,
        }
