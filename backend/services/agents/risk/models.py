from dataclasses import dataclass, field
from typing import Dict


@dataclass
class RiskDetail:
    category: str
    level: str
    score: float
    reason: str


@dataclass
class RiskResult:
    scenario: str
    financial_risk: str
    market_risk: str
    competition_risk: str
    customer_risk: str
    operational_risk: str
    overall_score: float
    overall_level: str
    confidence: str
    details: Dict[str, RiskDetail] = field(default_factory=dict)

    def to_dict(self):
        return {
            "scenario": self.scenario,
            "financial_risk": self.financial_risk,
            "market_risk": self.market_risk,
            "competition_risk": self.competition_risk,
            "customer_risk": self.customer_risk,
            "operational_risk": self.operational_risk,
            "overall_score": self.overall_score,
            "overall_level": self.overall_level,
            "confidence": self.confidence,
            "reasons": {k: v.reason for k, v in self.details.items()},
        }
