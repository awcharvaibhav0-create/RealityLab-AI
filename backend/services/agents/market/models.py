from dataclasses import dataclass, field
from typing import Dict


@dataclass
class MarketResult:
    analysis_date: str = ""
    analysis_time: str = ""
    season: str = ""
    day_type: str = ""
    market_trend: str = ""
    demand: str = ""
    competition: str = ""
    market_score: float = 0.0
    confidence: str = "Medium"
    assumptions: Dict[str, float] = field(default_factory=dict)

    def to_dict(self):
        return {
            "analysis_date": self.analysis_date,
            "analysis_time": self.analysis_time,
            "season": self.season,
            "day_type": self.day_type,
            "market_trend": self.market_trend,
            "demand": self.demand,
            "competition": self.competition,
            "market_score": self.market_score,
            "confidence": self.confidence,
            "assumptions": self.assumptions,
        }
