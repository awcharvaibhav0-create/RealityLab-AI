from typing import Any
from backend.services.core.base_agent import BaseAgent
from backend.services.core.types import Context, ReturnType
from .market_engine import MarketEngine
from .validator import MarketValidator


class MarketAgent(BaseAgent):
    """
    Market Intelligence Agent for the RealityLab AI project.
    Analyzes current market conditions using local rules and context.
    """

    def __init__(self, name: str = "MarketAgent"):
        super().__init__(name)
        self.engine = MarketEngine()
        self.validator = MarketValidator()

    def _do_initialize(self, config: Context) -> None:
        """Initialize the market agent with configuration."""
        pass

    def _do_execute(self, task: Any, context: Context) -> ReturnType:
        """Execute market analysis task."""
        self.validator.validate(task)
        result = self.engine.analyze(task)
        return {
            "market_score": result.market_score,
            "market_trend": result.market_trend,
            "metadata": {"status": "success"},
        }
