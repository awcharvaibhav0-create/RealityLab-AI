class InvestmentCalculator:
    @staticmethod
    def calculate(capital: float, additional_costs: float = 0.0) -> float:
        """Calculate total initial investment."""
        return capital + additional_costs
