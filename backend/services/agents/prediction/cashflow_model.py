from typing import List


class CashflowModel:
    def project_cashflow(
        self, revenue: List[float], expenses: List[float]
    ) -> List[float]:
        if len(revenue) != len(expenses):
            raise ValueError("Revenue and expenses length must match")
        return [r - e for r, e in zip(revenue, expenses)]
