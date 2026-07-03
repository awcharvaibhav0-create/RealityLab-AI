from dataclasses import dataclass, field
from typing import Dict


@dataclass
class RevenueResult:
    total_revenue: float
    breakdown: Dict[str, float] = field(default_factory=dict)


@dataclass
class ExpenseResult:
    total_expenses: float
    fixed_costs: float
    variable_costs: float
    breakdown: Dict[str, float] = field(default_factory=dict)


@dataclass
class FinanceResult:
    scenario: str
    projected_revenue: Dict[str, float]
    projected_profit: Dict[str, float]
    roi: str
    break_even: str
    cash_flow: str
    confidence: str

    def to_dict(self):
        return {
            "scenario": self.scenario,
            "projected_revenue": self.projected_revenue,
            "projected_profit": self.projected_profit,
            "roi": self.roi,
            "break_even": self.break_even,
            "cash_flow": self.cash_flow,
            "confidence": self.confidence,
        }
