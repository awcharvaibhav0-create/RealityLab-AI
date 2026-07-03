from typing import List, Dict
from .models import ScenarioOutput, Recommendation
from .score_normalizer import ScoreNormalizer
from .weight_manager import WeightManager
from .composite_calculator import CompositeCalculator
from .ranking_engine import RankingEngine
from .recommendation_builder import RecommendationBuilder
from .validator import Validator


class ScoreEngine:
    """Core engine orchestrating the scoring process."""

    def __init__(
        self,
        validator: Validator,
        normalizer: ScoreNormalizer,
        weight_manager: WeightManager,
        calculator: CompositeCalculator,
        ranking_engine: RankingEngine,
        builder: RecommendationBuilder,
    ):
        self.validator = validator
        self.normalizer = normalizer
        self.weight_manager = weight_manager
        self.calculator = calculator
        self.ranking_engine = ranking_engine
        self.builder = builder

    def run(
        self, scenarios: List[ScenarioOutput], weights_dict: Dict[str, float]
    ) -> Recommendation:
        """Runs the complete evaluation pipeline."""
        self.validator.validate_scenarios(scenarios)
        self.validator.validate_weights(weights_dict)

        normalized = self.normalizer.normalize(scenarios)
        weights = self.weight_manager.process_weights(weights_dict)

        composite_scores = self.calculator.calculate(normalized, weights)
        rankings = self.ranking_engine.rank(composite_scores)

        return self.builder.build(rankings)
