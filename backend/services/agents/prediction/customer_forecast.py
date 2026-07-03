from datetime import datetime, timedelta
from backend.services.agents.prediction.models import ForecastInput, ForecastOutput
from backend.services.agents.prediction.customer_model import CustomerModel


class CustomerForecaster:
    def forecast(
        self, input_data: ForecastInput, customer_model: CustomerModel
    ) -> ForecastOutput:
        initial_customers = int(input_data.historical_data.get("customers", 0))
        values_int = customer_model.project_customers(
            initial_customers, input_data.time_horizon_months
        )
        values = [float(v) for v in values_int]
        time_points = [
            datetime.now() + timedelta(days=30 * i)
            for i in range(1, input_data.time_horizon_months + 1)
        ]
        return ForecastOutput(
            metric_name="Customers", values=values, time_points=time_points
        )
