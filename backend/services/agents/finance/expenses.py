from typing import Dict
from .models import ExpenseResult


class ExpenseCalculator:
    @staticmethod
    def calculate(
        fixed_costs: Dict[str, float], variable_cost_per_unit: float, units_sold: float
    ) -> ExpenseResult:
        """Calculate total expenses."""
        total_fixed = sum(fixed_costs.values())
        total_variable = variable_cost_per_unit * units_sold
        total = total_fixed + total_variable
        breakdown = {
            "total_fixed": total_fixed,
            "total_variable": total_variable,
            **fixed_costs,
        }

        return ExpenseResult(
            total_expenses=total,
            fixed_costs=total_fixed,
            variable_costs=total_variable,
            breakdown=breakdown,
        )
