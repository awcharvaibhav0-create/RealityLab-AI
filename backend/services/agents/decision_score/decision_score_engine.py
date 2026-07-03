from typing import List, Dict
from .models import ScenarioOutput, Recommendation
from .score_engine import ScoreEngine


class DecisionScoreEngine:
    """Facade for the scoring system."""

    def __init__(self, score_engine: ScoreEngine):
        self.score_engine = score_engine

    def evaluate(
        self, scenarios: List[ScenarioOutput], weights: Dict[str, float]
    ) -> Recommendation:
        """Evaluates scenario outputs and selects the optimal business strategy."""
        return self.score_engine.run(scenarios, weights)
