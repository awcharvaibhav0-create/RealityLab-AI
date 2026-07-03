from typing import Dict, Any


class FeedbackCollector:
    """Collects structured user feedback and actual business outcomes."""

    def collect(self, feedback_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates and formats the feedback input.
        """
        required_fields = ["analysis_id", "implemented", "user_satisfaction"]

        for field in required_fields:
            if field not in feedback_json:
                raise ValueError(f"Missing required feedback field: {field}")

        # Format for downstream processing
        return {
            "analysis_id": feedback_json["analysis_id"],
            "implemented": feedback_json["implemented"],
            "user_satisfaction": feedback_json["user_satisfaction"],
            "actual_metrics": feedback_json.get("actual", {}),
            "comments": feedback_json.get("comments", ""),
        }
