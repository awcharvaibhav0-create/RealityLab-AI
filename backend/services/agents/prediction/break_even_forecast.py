from backend.services.agents.prediction.models import ForecastOutput


class BreakEvenForecaster:
    def calculate_break_even_month(
        self, profit_out: ForecastOutput, initial_investment: float
    ) -> int:
        cumulative_profit = 0.0
        for i, profit in enumerate(profit_out.values, start=1):
            cumulative_profit += profit
            if cumulative_profit >= initial_investment:
                return i
        return -1
