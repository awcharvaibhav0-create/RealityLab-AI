from typing import Dict, Any


def validate_scenario_schema(scenario: Dict[str, Any]) -> bool:
    """Validates the structure of the business scenario dictionary."""
    if not isinstance(scenario, dict):
        return False

    required_keys = ["id", "description"]
    for key in required_keys:
        if key not in scenario:
            return False

    return True
