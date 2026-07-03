from typing import Dict, Optional
from backend.services.agents.prediction.models import (
    ForecastInput,
    ForecastOutput,
    Scenario,
)
from backend.services.agents.prediction.growth_model import GrowthModel
from backend.services.agents.prediction.customer_model import CustomerModel
from backend.services.agents.prediction.cashflow_model import CashflowModel
from backend.services.agents.prediction.revenue_forecast import RevenueForecaster
from backend.services.agents.prediction.expense_forecast import ExpenseForecaster
from backend.services.agents.prediction.profit_forecast import ProfitForecaster
from backend.services.agents.prediction.customer_forecast import CustomerForecaster
from backend.services.agents.prediction.confidence_engine import ConfidenceEngine
from backend.services.agents.prediction.scenario_adjustment import ScenarioAdjuster


class ForecastEngine:
    def __init__(
        self, confidence_engine: ConfidenceEngine, scenario_adjuster: ScenarioAdjuster
    ):
        self.confidence_engine = confidence_engine
        self.scenario_adjuster = scenario_adjuster

        self.revenue_forecaster = RevenueForecaster()
        self.expense_forecaster = ExpenseForecaster()
        self.cashflow_model = CashflowModel()
        self.profit_forecaster = ProfitForecaster(self.cashflow_model)
        self.customer_forecaster = CustomerForecaster()

    def run_forecasts(
        self, input_data: ForecastInput, scenario: Optional[Scenario] = None
    ) -> Dict[str, ForecastOutput]:
        growth_rate = input_data.assumptions.get("growth_rate", 0.05)
        growth_model = GrowthModel(base_rate=growth_rate)

        churn_rate = input_data.assumptions.get("churn_rate", 0.02)
        acq_rate = input_data.assumptions.get("acquisition_rate", 0.05)
        customer_model = CustomerModel(churn_rate=churn_rate, acquisition_rate=acq_rate)

        revenue_out = self.revenue_forecaster.forecast(input_data, growth_model)
        expense_out = self.expense_forecaster.forecast(input_data, growth_model)
        profit_out = self.profit_forecaster.forecast(revenue_out, expense_out)
        customer_out = self.customer_forecaster.forecast(input_data, customer_model)

        results = {
            "revenue": revenue_out,
            "expense": expense_out,
            "profit": profit_out,
            "customers": customer_out,
        }

        variance = input_data.assumptions.get("variance", 0.1)

        for metric, out in results.items():
            if scenario:
                out.values = self.scenario_adjuster.apply_scenario(
                    out.values, scenario, metric
                )

            confidence = self.confidence_engine.generate_intervals(out.values, variance)
            out.confidence_intervals = confidence.bounds

        return results
