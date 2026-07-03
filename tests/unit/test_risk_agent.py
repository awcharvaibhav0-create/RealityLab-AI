import pytest
from backend.services.agents.risk import RiskAgent, RiskValidationError


@pytest.fixture
def risk_agent():
    agent = RiskAgent()
    agent.initialize({})
    return agent


def test_risk_agent_initialization(risk_agent):
    assert risk_agent.name == "RiskAgent"
    assert len(risk_agent.evaluators) == 10


def test_risk_agent_validation(risk_agent):
    # Missing required keys
    with pytest.raises(RiskValidationError):
        risk_agent.validate({})

    # Valid schema
    scenario = {"id": "scenario_1", "description": "Test Scenario"}
    assert risk_agent.validate(scenario) is True


def test_risk_agent_execution(risk_agent):
    scenario = {
        "id": "scenario_1",
        "description": "Test",
        "financials": {"budget": 100, "estimated_cost": 120},
        "market": {"volatility": "high"},
        "operations": {"complexity": "high"},
    }

    result = risk_agent.execute(scenario)
    assert result["status"] == "success"

    risk_result = result["data"]

    # Assert on confidence score since partial data provided
    assert risk_result.confidence in ["Medium", "High"]

    # Financial should be high due to cost > budget
    financial_detail = risk_result.details["FINANCIAL"]
    assert financial_detail.score >= 50

    # Check overall score
    assert risk_result.overall_score > 0
