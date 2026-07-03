from typing import Dict, Any
from .feedback_collector import FeedbackCollector
from .accuracy_analyzer import AccuracyAnalyzer
from .suggestion_generator import SuggestionGenerator


class LearningEngine:
    """Coordinates feedback collection, accuracy analysis, and suggestion generation."""

    def __init__(self):
        self.feedback_collector = FeedbackCollector()
        self.accuracy_analyzer = AccuracyAnalyzer()
        self.suggestion_generator = SuggestionGenerator()

    def process_feedback(
        self,
        feedback_json: Dict[str, Any],
        projected_metrics: Dict[str, float],
        risk_realized: bool = False,
    ) -> Dict[str, Any]:
        """
        Main entry point for processing feedback.
        Returns a LearningSummary dictionary.
        """
        # 1. Collect and validate feedback
        collected = self.feedback_collector.collect(feedback_json)

        actual_metrics = collected["actual_metrics"]
        user_satisfaction = collected["user_satisfaction"]
        implemented = collected["implemented"]

        # If not implemented, learning is limited
        if not implemented:
            return {
                "forecast_accuracy": 0.0,
                "recommendation_success": 0.0,
                "improvement_suggestions": [
                    "Scenario was not implemented. No metrics available."
                ],
            }

        # 2. Analyze Accuracy
        accuracy = self.accuracy_analyzer.calculate_accuracy(
            projected_metrics, actual_metrics
        )

        # 3. Calculate Recommendation Success
        success = self.accuracy_analyzer.calculate_recommendation_success(
            accuracy, user_satisfaction, risk_realized
        )

        # 4. Generate Suggestions
        suggestions = self.suggestion_generator.generate_suggestions(
            projected_metrics, actual_metrics
        )

        # Return structured JSON
        return {
            "forecast_accuracy": round(accuracy, 2),
            "recommendation_success": round(success, 2),
            "improvement_suggestions": suggestions,
        }
