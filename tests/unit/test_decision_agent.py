import pytest
from unittest.mock import patch
from backend.services.agents.decision.decision_agent import DecisionAgent


@pytest.fixture
def agent():
    return DecisionAgent()


def test_decision_agent_success(agent):
    context_data = {"revenue": 1000, "costs": 800}

    mock_response = """
    {
        "decision": "Go",
        "score": 85,
        "confidence": "High",
        "explainability": ["Positive margin"],
        "executive_recommendations": ["Proceed with expansion"]
    }
    """

    with patch.object(
        agent.api_client,
        "generate_content",
        return_value=(
            mock_response,
            {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
        ),
    ) as mock_api:
        result = agent.generate_recommendation(context_data)

        mock_api.assert_called_once()
        assert "Proceed with expansion" in result


def test_decision_agent_fallback(agent):
    context_data = {"revenue": 1000}

    with patch.object(
        agent.api_client, "generate_content", side_effect=Exception("API Down")
    ):
        result = agent.generate_recommendation(context_data)

        assert "Escalate to human analyst" in result
        assert "API Down" in result
