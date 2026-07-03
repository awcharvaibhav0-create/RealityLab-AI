from backend.services.agents.prediction.models import ForecastOutput
from backend.services.agents.prediction.cashflow_model import CashflowModel


class CashflowForecaster:
    def __init__(self, cashflow_model: CashflowModel):
        self.cashflow_model = cashflow_model

    def forecast(
        self, inflows: ForecastOutput, outflows: ForecastOutput
    ) -> ForecastOutput:
        values = self.cashflow_model.project_cashflow(inflows.values, outflows.values)
        return ForecastOutput(
            metric_name="Net Cashflow", values=values, time_points=inflows.time_points
        )
