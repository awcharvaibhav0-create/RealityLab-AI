from typing import List


class GrowthModel:
    def __init__(self, base_rate: float):
        self.base_rate = base_rate

    def calculate_growth(self, initial_value: float, periods: int) -> List[float]:
        return [
            initial_value * ((1 + self.base_rate) ** i) for i in range(1, periods + 1)
        ]
