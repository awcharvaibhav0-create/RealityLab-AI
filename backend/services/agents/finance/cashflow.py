from typing import List


class CashflowCalculator:
    @staticmethod
    def calculate(
        initial_investment: float, revenues: List[float], expenses: List[float]
    ) -> List[float]:
        """
        Calculate cashflow over time given an initial investment and
        subsequent periodic revenues and expenses.
        """
        cashflow = [-initial_investment]
        for rev, exp in zip(revenues, expenses):
            cashflow.append(rev - exp)
        return cashflow
