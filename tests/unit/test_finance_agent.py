import pytest
from backend.services.agents.finance.finance_agent import FinanceAgent
from backend.services.agents.finance.models import FinanceResult


def test_finance_agent_initialization():
    agent = FinanceAgent("TestAgent")
    assert agent.name == "TestAgent"


def test_finance_agent_validation():
    agent = FinanceAgent("TestAgent")

    # Missing required fields should raise ValueError
    with pytest.raises(ValueError):
        agent.validate({"price_per_unit": 10})

    valid_task = {
        "price_per_unit": 10.0,
        "units_sold": 100,
        "fixed_costs": 200.0,
        "variable_cost_per_unit": 5.0,
        "initial_investment": 1000.0,
    }
    assert agent.validate(valid_task) is True


def test_finance_agent_execution():
    agent = FinanceAgent("TestAgent")
    agent.initialize({})
    valid_task = {
        "price_per_unit": 10.0,
        "units_sold": 100,
        "fixed_costs": 200.0,
        "variable_cost_per_unit": 5.0,
        "initial_investment": 1000.0,
        "periods": 1,
    }

    # Execution should return FinanceResult
    result = agent.execute(valid_task)
    assert isinstance(result, FinanceResult)

    # Check that months exist
    assert "month1" in result.projected_revenue
    assert "month1" in result.projected_profit

    # Profit = 1000 - 700 = 300 for month 1
    assert result.projected_profit["month1"] == 300.0

    # ROI = 1000 / 300 = 3.33 months
    assert "3 months" in result.roi

    # Break even
    assert "3 months" in result.break_even

    # Cashflow
    assert result.cash_flow == "Positive"
