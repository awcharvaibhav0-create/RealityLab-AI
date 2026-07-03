from typing import Dict


class AccuracyAnalyzer:
    """Compares projected metrics with actual metrics."""

    def calculate_accuracy(
        self, projected: Dict[str, float], actual: Dict[str, float]
    ) -> float:
        """
        Calculates the forecast accuracy score.
        1.0 means perfect accuracy.
        Lower values mean less accuracy.
        """
        if not projected or not actual:
            return 0.0

        accuracies = []
        for key, proj_val in projected.items():
            if key in actual:
                act_val = actual[key]
                if proj_val == 0 and act_val == 0:
                    accuracies.append(1.0)
                elif proj_val == 0:
                    accuracies.append(0.0)
                else:
                    # e.g., 91000 / 95000 = 0.957
                    ratio = act_val / proj_val
                    # Accuracy should penalize both over and under estimation, but for simplicity
                    # we'll just take the min ratio if it's over 1
                    if ratio > 1.0:
                        ratio = 1.0 / ratio
                    accuracies.append(ratio)

        if not accuracies:
            return 0.0

        return sum(accuracies) / len(accuracies)

    def calculate_recommendation_success(
        self, accuracy: float, user_satisfaction: str, risk_realized: bool
    ) -> float:
        """
        Calculates the overall recommendation success score based on multiple factors.
        """
        satisfaction_scores = {
            "Very Satisfied": 1.0,
            "Satisfied": 0.8,
            "Neutral": 0.5,
            "Dissatisfied": 0.2,
        }

        sat_score = satisfaction_scores.get(user_satisfaction, 0.5)
        risk_penalty = 0.8 if risk_realized else 1.0

        # 60% accuracy, 40% satisfaction
        base_score = (accuracy * 0.6) + (sat_score * 0.4)
        return base_score * risk_penalty
