from typing import Dict, Any


class ReportSchemaValidator:
    """Basic schema validation for report input data."""

    @staticmethod
    def validate(data: Dict[str, Any]) -> bool:
        if "title" not in data or "author" not in data:
            return False
        return True
