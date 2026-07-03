from typing import List
from .models import CompositeScore


class TieBreaker:
    """Resolves ties between competing strategies."""

    def resolve_ties(self, scores: List[CompositeScore]) -> List[CompositeScore]:
        """Sorts scores by total_score descending, then by overall_confidence descending."""
        return sorted(
            scores, key=lambda x: (x.total_score, x.overall_confidence), reverse=True
        )
