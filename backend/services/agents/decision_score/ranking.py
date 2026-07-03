from typing import List
from .models import StrategyRanking


class Ranking:
    """Domain model representing the final strategy rankings."""

    def __init__(self, rankings: List[StrategyRanking]):
        self.rankings = rankings

    def get_top_ranking(self) -> StrategyRanking:
        if not self.rankings:
            raise ValueError("No rankings available")
        return self.rankings[0]
