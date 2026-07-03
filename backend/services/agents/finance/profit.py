class ProfitCalculator:
    @staticmethod
    def calculate(total_revenue: float, total_expenses: float) -> float:
        """Calculate net profit."""
        return total_revenue - total_expenses
