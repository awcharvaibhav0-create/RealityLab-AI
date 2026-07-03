from .models import RecommendationDecision


class FallbackEngine:
    def get_fallback_decision(self, error_message: str) -> RecommendationDecision:
        """Provides a safe fallback recommendation when API fails."""
        return RecommendationDecision(
            decision="No-Go",
            score=0,
            confidence="Low",
            explainability=[f"Automated decision failed: {error_message}"],
            executive_recommendations=["Escalate to human analyst for manual review"],
        )
