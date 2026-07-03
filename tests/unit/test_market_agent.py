from backend.services.agents.market.market_agent import MarketAgent
from backend.services.core.constants import AgentState


def test_market_agent_initialization():
    agent = MarketAgent("TestMarketAgent")
    agent.initialize({})
    assert agent.name == "TestMarketAgent"
    assert agent.state == AgentState.INITIALIZED


def test_market_agent_execute():
    agent = MarketAgent()
    agent.initialize({})
    result = agent.execute({"competitor_count": 2})
    assert "market_score" in result
    assert "market_trend" in result
    assert "metadata" in result
    assert result["metadata"]["status"] == "success"
