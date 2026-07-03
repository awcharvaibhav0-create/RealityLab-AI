from .models import RecommendationDecision


class Formatter:
    def format_recommendation(self, decision: RecommendationDecision) -> str:
        """Formats the decision into a human-readable executive recommendation string."""
        import json

        # Since SRS specifies JSON output format for this agent's API response,
        # we can just return it as a JSON string, or a formatted string.
        # I'll provide a clean string and the JSON.

        return json.dumps(decision.model_dump(), indent=2)
