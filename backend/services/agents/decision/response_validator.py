from typing import Dict, Any
from .models import RecommendationDecision


class ResponseValidator:
    def validate(self, parsed_response: Dict[str, Any]) -> RecommendationDecision:
        """Validates the parsed dictionary and returns a RecommendationDecision model."""
        return RecommendationDecision(**parsed_response)
