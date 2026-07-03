import re
from typing import Dict, Any


class InputValidator:
    """Validates inputs before they reach agents."""

    def __init__(self):
        # Basic SQL injection prevention patterns
        self.sql_injection_pattern = re.compile(
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE)\b)|(--)|(;)",
            re.IGNORECASE,
        )

    def validate_numeric(
        self, value: Any, min_val: float = None, max_val: float = None
    ) -> bool:
        """Validates numeric ranges."""
        try:
            num = float(value)
            if min_val is not None and num < min_val:
                return False
            if max_val is not None and num > max_val:
                return False
            return True
        except (ValueError, TypeError):
            return False

    def validate_string(self, value: Any, max_length: int = 1000) -> bool:
        """Validates strings for length and basic injection patterns."""
        if not isinstance(value, str):
            return False

        if len(value) > max_length:
            return False

        # Reject obvious SQL injection patterns
        if self.sql_injection_pattern.search(value):
            return False

        return True

    def validate_business_profile(self, profile: Dict[str, Any]) -> bool:
        """Validates a complete business profile payload."""
        required_fields = ["id", "name", "type", "location"]

        for field in required_fields:
            if field not in profile:
                return False

        if not self.validate_string(profile["name"], max_length=100):
            return False

        return True
