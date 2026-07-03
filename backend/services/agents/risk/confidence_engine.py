from typing import Dict, Any


class ConfidenceEngine:
    def calculate_confidence(self, scenario: Dict[str, Any]) -> float:
        """
        Calculate confidence score based on completeness of scenario data.
        Returns a value between 0.0 and 1.0.
        """
        expected_keys = [
            "financials",
            "market",
            "operations",
            "customer",
            "execution",
            "competition",
            "seasonal",
            "supply_chain",
            "regulatory",
            "business_continuity",
        ]

        found = sum(1 for key in expected_keys if key in scenario)
        confidence = found / len(expected_keys) if expected_keys else 1.0

        # Ensure it's never 0 if some data is present
        return max(0.1, confidence)
