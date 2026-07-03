from typing import Any


class MarketValidator:
    """Validates input data for the market agent."""

    def validate(self, data: Any) -> bool:
        if not isinstance(data, dict):
            raise ValueError("Task data must be a dictionary")
        return True
