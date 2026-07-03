from backend.services.agents.prediction.models import ForecastOutput
from backend.services.agents.prediction.cashflow_model import CashflowModel


class ProfitForecaster:
    def __init__(self, cashflow_model: CashflowModel):
        self.cashflow_model = cashflow_model

    def forecast(
        self, revenue_out: ForecastOutput, expense_out: ForecastOutput
    ) -> ForecastOutput:
        values = self.cashflow_model.project_cashflow(
            revenue_out.values, expense_out.values
        )
        return ForecastOutput(
            metric_name="Profit", values=values, time_points=revenue_out.time_points
        )
