from .models import Recommendation
from .ranking import Ranking


class RecommendationBuilder:
    """Builds the final recommendation based on rankings."""

    def build(self, ranking: Ranking) -> Recommendation:
        top = ranking.get_top_ranking()

        rationale = (
            f"Strategy {top.strategy_id} selected with score "
            f"{top.score.total_score:.2f} and confidence {top.score.overall_confidence:.2f}."
        )

        return Recommendation(
            recommended_strategy_id=top.strategy_id,
            rankings=ranking.rankings,
            rationale=rationale,
        )
