class ROICalculator:
    @staticmethod
    def calculate(net_profit: float, total_investment: float) -> float:
        """Calculate Return on Investment (ROI) as a percentage."""
        if total_investment == 0:
            return 0.0
        return (net_profit / total_investment) * 100.0
