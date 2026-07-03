class RealityLabError(Exception):
    """Base exception for all RealityLab AI project errors."""

    pass


class AgentError(RealityLabError):
    """Base exception for agent-related errors."""

    pass


class AgentInitializationError(AgentError):
    """Raised when an agent fails to initialize."""

    pass


class AgentExecutionError(AgentError):
    """Raised when an agent fails during execution."""

    pass


class ValidationError(RealityLabError):
    """Raised when validation fails."""

    pass


class ConfigurationError(RealityLabError):
    """Raised for configuration errors."""

    pass
