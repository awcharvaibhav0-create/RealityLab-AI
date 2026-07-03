from typing import Any
from .interfaces import IValidator
from .exceptions import ValidationError


class BaseValidator(IValidator):
    """Base implementation for a generic validator."""

    def __init__(self) -> None:
        self._rules = []

    def add_rule(self, rule: callable) -> None:
        """Add a validation rule."""
        self._rules.append(rule)

    def validate(self, data: Any) -> bool:
        """
        Validate the data against all registered rules.
        Raises ValidationError if any rule fails.
        """
        for rule in self._rules:
            if not rule(data):
                raise ValidationError(
                    f"Validation failed for data: {data} against rule: {rule.__name__}"
                )
        return True
