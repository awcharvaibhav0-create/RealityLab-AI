import unittest
from typing import Dict, Any

from backend.services.engines.simulation.models import Scenario, ScenarioStatus
from backend.services.engines.simulation.scenario_engine import ScenarioSimulationEngine
from backend.services.engines.simulation.scenario_builder import ScenarioBuilder


class TestScenarioEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ScenarioSimulationEngine()

    def test_run_scenario_default_handler(self):
        builder = ScenarioBuilder("Test Scenario")
        builder.with_context_variable("input_a", 10)
        scenario = builder.build()

        result = self.engine.run_scenario(scenario)

        self.assertEqual(result.status, ScenarioStatus.COMPLETED)
        self.assertIn("time_series", result.output_state)
        self.assertIn("final_state", result.output_state)

    def test_run_scenario_custom_handler(self):
        def custom_handler(s: Scenario) -> Dict[str, Any]:
            val = s.context.variables.get("val", 0)
            return {"state": {"result": val * 2}, "metrics": {"custom_metric": 42.0}}

        self.engine.register_execution_handler("custom", custom_handler)

        scenario = ScenarioBuilder("Custom").with_context_variable("val", 5).build()
        result = self.engine.run_scenario(scenario, handler_name="custom")

        self.assertEqual(result.status, ScenarioStatus.COMPLETED)
        self.assertEqual(result.output_state["result"], 10)
        self.assertEqual(result.metrics["custom_metric"], 42.0)

    def test_insufficient_resources(self):
        scenario = (
            ScenarioBuilder("Huge Scenario").with_resources(cpu_cores=100.0).build()
        )
        result = self.engine.run_scenario(scenario)

        self.assertEqual(result.status, ScenarioStatus.FAILED)
        self.assertEqual(result.error_message, "Insufficient resources.")
