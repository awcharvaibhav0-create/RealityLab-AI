from typing import List
from collections import defaultdict
from .models import NormalizedScore, CompositeScore
from .weights import Weights
from .confidence_aggregator import ConfidenceAggregator


class CompositeCalculator:
    """Calculates final composite scores per strategy."""

    def __init__(self, confidence_aggregator: ConfidenceAggregator):
        self.confidence_aggregator = confidence_aggregator

    def calculate(
        self, normalized: List[NormalizedScore], weights: Weights
    ) -> List[CompositeScore]:
        strategy_metrics = defaultdict(list)
        strategy_confidences = defaultdict(list)

        for score in normalized:
            strategy_metrics[score.strategy_id].append(score.normalized_metrics)
            strategy_confidences[score.strategy_id].append(score.confidence)

        results = []
        for strategy_id, metrics_list in strategy_metrics.items():
            if not metrics_list:
                continue

            # Average the metrics across scenarios for this strategy
            avg_metrics = {}
            for key in metrics_list[0].keys():
                avg_metrics[key] = sum(m[key] for m in metrics_list) / len(metrics_list)

            total_score = sum(avg_metrics[k] * weights.get(k) for k in avg_metrics)

            # Simple average for overall confidence per strategy
            avg_conf = sum(strategy_confidences[strategy_id]) / len(
                strategy_confidences[strategy_id]
            )

            # Penalize/Boost total score based on confidence
            adjusted_total = total_score * avg_conf

            results.append(
                CompositeScore(
                    strategy_id=strategy_id,
                    total_score=adjusted_total,
                    component_scores=avg_metrics,
                    overall_confidence=avg_conf,
                )
            )

        return results
