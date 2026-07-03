import unittest
from backend.services.agents.prediction.models import ForecastInput, Scenario
from backend.services.agents.prediction.prediction_agent import PredictionAgent
from backend.services.agents.prediction.validator import InputValidator
from backend.services.agents.prediction.growth_model import GrowthModel
from backend.services.agents.prediction.cashflow_model import CashflowModel


class TestPredictionAgent(unittest.TestCase):

    def setUp(self):
        self.agent = PredictionAgent()
        self.valid_input = ForecastInput(
            historical_data={"revenue": 10000.0, "expense": 5000.0, "customers": 100.0},
            time_horizon_months=12,
            assumptions={
                "growth_rate": 0.1,
                "variance": 0.05,
                "churn_rate": 0.02,
                "acquisition_rate": 0.1,
            },
        )

    def test_predict_success(self):
        result = self.agent.predict(self.valid_input)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["time_horizon_months"], 12)

        forecasts = result["forecasts"]
        self.assertIn("revenue", forecasts)
        self.assertIn("expense", forecasts)
        self.assertIn("profit", forecasts)
        self.assertIn("customers", forecasts)

        # Check lengths match time horizon
        self.assertEqual(len(forecasts["revenue"].values), 12)

        # Check confidence intervals
        self.assertIn("upper", forecasts["revenue"].confidence_intervals)
        self.assertIn("lower", forecasts["revenue"].confidence_intervals)

    def test_scenario_adjustment(self):
        scenario = Scenario(name="Optimistic", adjustments={"revenue": 1.2})
        result = self.agent.predict(self.valid_input, scenario)

        # Original without scenario should be lower
        base_result = self.agent.predict(self.valid_input)

        self.assertGreater(
            result["forecasts"]["revenue"].values[0],
            base_result["forecasts"]["revenue"].values[0],
        )


class TestValidator(unittest.TestCase):
    def test_invalid_horizon(self):
        validator = InputValidator()
        invalid_input = ForecastInput(
            historical_data={"revenue": 1000.0}, time_horizon_months=-1
        )
        with self.assertRaises(ValueError):
            validator.validate(invalid_input)

    def test_empty_historical_data(self):
        validator = InputValidator()
        invalid_input = ForecastInput(historical_data={}, time_horizon_months=12)
        with self.assertRaises(ValueError):
            validator.validate(invalid_input)


class TestModels(unittest.TestCase):
    def test_growth_model(self):
        model = GrowthModel(base_rate=0.1)
        values = model.calculate_growth(100.0, 3)
        self.assertEqual(len(values), 3)
        self.assertAlmostEqual(values[0], 110.0)
        self.assertAlmostEqual(values[1], 121.0)

    def test_cashflow_model(self):
        model = CashflowModel()
        rev = [100.0, 200.0]
        exp = [50.0, 100.0]
        cf = model.project_cashflow(rev, exp)
        self.assertEqual(cf, [50.0, 100.0])


if __name__ == "__main__":
    unittest.main()
