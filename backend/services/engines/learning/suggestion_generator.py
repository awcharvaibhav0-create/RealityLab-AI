from typing import List, Dict


class SuggestionGenerator:
    """Generates improvement suggestions based on analysis deviations."""

    def generate_suggestions(
        self, projected: Dict[str, float], actual: Dict[str, float]
    ) -> List[str]:
        """
        Analyzes the deviations and generates actionable suggestions for human review.
        """
        suggestions = []

        if not projected or not actual:
            return ["Insufficient data for suggestion generation."]

        for key, proj_val in projected.items():
            if key in actual:
                act_val = actual[key]
                if proj_val > 0:
                    diff_pct = (act_val - proj_val) / proj_val

                    # If actual is 20% lower than projected
                    if diff_pct < -0.2:
                        suggestions.append(
                            f"Review {key} assumptions: Actual was significantly lower than projected."
                        )
                    # If actual is 20% higher than projected
                    elif diff_pct > 0.2:
                        suggestions.append(
                            f"Review {key} assumptions: Actual was significantly higher than projected."
                        )

        if not suggestions:
            suggestions.append(
                "Forecast was accurate. No immediate rule changes suggested."
            )

        return suggestions
