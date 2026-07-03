import pytest
from backend.services.core.constants import AgentState
from backend.services.core.exceptions import (
    AgentInitializationError,
    AgentExecutionError,
    ValidationError,
)
from backend.services.core.validator import BaseValidator
from backend.services.core.base_agent import BaseAgent


class MockAgent(BaseAgent):
    def _do_initialize(self, config):
        if config.get("fail_init"):
            raise ValueError("Init failure")

    def _do_execute(self, task, context):
        if task == "fail":
            raise RuntimeError("Execute failure")
        return f"Processed {task}"


def test_base_agent_lifecycle():
    agent = MockAgent("test_agent")
    assert agent.state == AgentState.IDLE

    agent.initialize({"key": "value"})
    assert agent.state == AgentState.INITIALIZED

    result = agent.execute("test_task")
    assert result == "Processed test_task"
    assert agent.state == AgentState.IDLE

    assert agent.health_check() is True

    agent.cleanup()
    assert agent.state == AgentState.STOPPED


def test_base_agent_init_failure():
    agent = MockAgent("fail_agent")
    with pytest.raises(AgentInitializationError):
        agent.initialize({"fail_init": True})
    assert agent.state == AgentState.ERROR
    assert agent.health_check() is False


def test_base_agent_execute_failure():
    agent = MockAgent("fail_exec_agent")
    agent.initialize({})
    with pytest.raises(AgentExecutionError):
        agent.execute("fail")
    assert agent.state == AgentState.ERROR


def test_validator():
    validator = BaseValidator()
    validator.add_rule(lambda x: isinstance(x, int))
    validator.add_rule(lambda x: x > 0)

    assert validator.validate(5) is True

    with pytest.raises(ValidationError):
        validator.validate(-1)

    with pytest.raises(ValidationError):
        validator.validate("string")
