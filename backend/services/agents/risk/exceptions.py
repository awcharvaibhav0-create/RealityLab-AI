class RiskException(Exception):
    """Base exception for Risk Agent."""

    pass


class RiskValidationError(RiskException):
    """Raised when scenario validation fails."""

    pass


class RiskCalculationError(RiskException):
    """Raised when risk calculation fails."""

    pass
