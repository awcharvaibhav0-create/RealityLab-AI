import logging
from abc import ABC, abstractmethod
from typing import Any, Optional
from .interfaces import IAgent
from .types import Context, ReturnType
from .constants import AgentState
from .exceptions import AgentInitializationError, AgentExecutionError

logger = logging.getLogger(__name__)


class BaseAgent(IAgent, ABC):
    """
    Base implementation for all agents in the RealityLab AI framework.
    Provides lifecycle management including initialize, execute, validate, cleanup, and health_check.
    """

    def __init__(self, name: str):
        self.name = name
        self.state: AgentState = AgentState.IDLE
        self.context: Context = {}

    def initialize(self, config: Context) -> None:
        """Initialize the agent with the provided configuration."""
        try:
            self.context.update(config)
            self._do_initialize(config)
            self.state = AgentState.INITIALIZED
            logger.info(f"Agent {self.name} initialized successfully.")
        except Exception as e:
            self.state = AgentState.ERROR
            logger.error(f"Failed to initialize agent {self.name}: {e}")
            raise AgentInitializationError(f"Initialization failed: {e}") from e

    def execute(self, task: Any, context: Optional[Context] = None) -> ReturnType:
        """Execute a task."""
        if self.state not in [
            AgentState.INITIALIZED,
            AgentState.IDLE,
            AgentState.STOPPED,
        ]:
            raise AgentExecutionError(
                f"Cannot execute task, agent {self.name} is in state {self.state.value}"
            )

        self.state = AgentState.RUNNING
        try:
            self.validate(task)
            result = self._do_execute(task, context or {})
            self.state = AgentState.IDLE
            return result
        except Exception as e:
            self.state = AgentState.ERROR
            logger.error(f"Execution failed for agent {self.name}: {e}")
            raise AgentExecutionError(f"Execution failed: {e}") from e

    def cleanup(self) -> None:
        """Cleanup agent resources."""
        try:
            self._do_cleanup()
            self.state = AgentState.STOPPED
            logger.info(f"Agent {self.name} cleanup completed.")
        except Exception as e:
            self.state = AgentState.ERROR
            logger.error(f"Cleanup failed for agent {self.name}: {e}")

    def health_check(self) -> bool:
        """Basic health check for the agent."""
        return self.state != AgentState.ERROR and self._do_health_check()

    def validate(self, task: Any) -> bool:
        """
        Validate a task before execution.
        Subclasses should override if specific validation is needed.
        """
        if task is None:
            raise ValueError("Task cannot be None")
        return True

    # Template methods for subclasses to implement
    @abstractmethod
    def _do_initialize(self, config: Context) -> None:
        pass

    @abstractmethod
    def _do_execute(self, task: Any, context: Context) -> ReturnType:
        pass

    def _do_cleanup(self) -> None:
        pass

    def _do_health_check(self) -> bool:
        return True
