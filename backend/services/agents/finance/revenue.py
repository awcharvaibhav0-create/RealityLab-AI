from typing import Dict
from .models import RevenueResult


class RevenueCalculator:
    @staticmethod
    def calculate(
        price_per_unit: float,
        units_sold: float,
        additional_revenue: Dict[str, float] = None,
    ) -> RevenueResult:
        """Calculate total revenue."""
        additional = additional_revenue or {}
        core_revenue = price_per_unit * units_sold
        total = core_revenue + sum(additional.values())
        breakdown = {"core_revenue": core_revenue, **additional}
        return RevenueResult(total_revenue=total, breakdown=breakdown)
