from abc import ABC, abstractmethod
from typing import Any, Optional
from .types import Context, ReturnType


class IValidator(ABC):
    """Interface for all validators."""

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate the given data."""
        pass


class IAgent(ABC):
    """Interface for an autonomous agent."""

    @abstractmethod
    def initialize(self, config: Context) -> None:
        """Initialize the agent with configuration."""
        pass

    @abstractmethod
    def execute(self, task: Any, context: Optional[Context] = None) -> ReturnType:
        """Execute a given task."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup resources used by the agent."""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check if the agent is healthy."""
        pass
