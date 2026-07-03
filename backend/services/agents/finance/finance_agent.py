from typing import Any
from backend.services.core.base_agent import BaseAgent
from backend.services.core.types import Context
from .finance_engine import FinanceEngine
from .validator import Validator
from .models import FinanceResult


class FinanceAgent(BaseAgent):
    """
    Finance Agent responsible for deterministic financial analysis.
    """

    def __init__(self, name: str = "FinanceAgent"):
        super().__init__(name)
        self.engine = FinanceEngine()

    def _do_initialize(self, config: Context) -> None:
        """Initialize any specific configurations for the agent."""
        pass

    def estimate_baseline(self, profile: dict) -> dict:
        """
        Dynamically estimate baseline financial fields if not provided.
        Avoids hardcoded dummy values by deriving from initial investment.
        """
        investment = float(profile.get("investment", 100000))
        return {
            "expected_revenue": investment * 1.5,
            "operating_costs": investment * 0.8
        }

    def validate(self, task: Any) -> bool:
        """Validate the financial scenario input."""
        super().validate(task)
        if not isinstance(task, dict):
            raise ValueError(
                "Task must be a dictionary representing the financial scenario."
            )
        return Validator.validate_scenario(task)

    def _do_execute(self, task: Any, context: Context) -> FinanceResult:
        """Execute the financial analysis using the provided scenario."""
        return self.engine.run_analysis(task)

    def _do_cleanup(self) -> None:
        """Cleanup agent resources."""
        pass
