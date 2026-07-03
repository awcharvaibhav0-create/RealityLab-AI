from typing import List
from .models import CompositeScore, StrategyRanking
from .tie_breaker import TieBreaker
from .ranking import Ranking


class RankingEngine:
    """Ranks the composite scores into a definitive list."""

    def __init__(self, tie_breaker: TieBreaker):
        self.tie_breaker = tie_breaker

    def rank(self, scores: List[CompositeScore]) -> Ranking:
        sorted_scores = self.tie_breaker.resolve_ties(scores)

        rankings = []
        for i, score in enumerate(sorted_scores):
            is_tie = False
            if i > 0:
                prev = sorted_scores[i - 1]
                if (
                    score.total_score == prev.total_score
                    and score.overall_confidence == prev.overall_confidence
                ):
                    is_tie = True

            rankings.append(
                StrategyRanking(
                    strategy_id=score.strategy_id,
                    rank=i + 1,
                    score=score,
                    is_tie=is_tie,
                )
            )

        return Ranking(rankings)
