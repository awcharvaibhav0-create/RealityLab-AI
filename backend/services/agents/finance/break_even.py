from typing import Optional


class BreakEvenCalculator:
    @staticmethod
    def calculate(
        fixed_costs: float, price_per_unit: float, variable_cost_per_unit: float
    ) -> Optional[float]:
        """Calculate break-even point in units."""
        contribution_margin = price_per_unit - variable_cost_per_unit
        if contribution_margin <= 0:
            return (
                None  # Break-even is impossible if variable costs exceed or equal price
            )
        return fixed_costs / contribution_margin
