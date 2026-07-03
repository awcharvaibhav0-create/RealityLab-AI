from typing import Any, Type, Union


class ValidationError(Exception):
    """Base exception for validation errors."""

    pass


def require_not_none(value: Any, name: str = "Value") -> Any:
    """Ensure value is not None."""
    if value is None:
        raise ValidationError(f"{name} cannot be None.")
    return value


def require_non_empty_string(value: Any, name: str = "String") -> str:
    """Ensure value is a non-empty string."""
    if not isinstance(value, str):
        raise ValidationError(f"{name} must be a string.")
    if not value.strip():
        raise ValidationError(f"{name} cannot be empty.")
    return value


def require_type(
    value: Any, expected_type: Union[Type, tuple], name: str = "Value"
) -> Any:
    """Ensure value is of expected type."""
    if not isinstance(value, expected_type):
        raise ValidationError(f"{name} must be of type {expected_type}.")
    return value


def require_in_range(
    value: Union[int, float],
    min_val: Union[int, float],
    max_val: Union[int, float],
    name: str = "Value",
) -> Union[int, float]:
    """Ensure numeric value is within range (inclusive)."""
    if not (min_val <= value <= max_val):
        raise ValidationError(f"{name} must be between {min_val} and {max_val}.")
    return value


def require_positive(
    value: Union[int, float], name: str = "Value"
) -> Union[int, float]:
    """Ensure numeric value is strictly positive (> 0)."""
    if value <= 0:
        raise ValidationError(f"{name} must be strictly positive.")
    return value
