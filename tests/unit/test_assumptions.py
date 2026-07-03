import unittest
from backend.services.engines.simulation.assumption_manager import AssumptionManager
from backend.services.engines.simulation.models import ScenarioAssumption


class TestAssumptionManager(unittest.TestCase):
    def setUp(self):
        self.manager = AssumptionManager()

    def test_add_and_get_assumption(self):
        assumption = ScenarioAssumption(name="inflation_rate", value=0.03)
        self.manager.add_assumption(assumption)

        retrieved = self.manager.get_assumption(assumption.name)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "inflation_rate")
        self.assertEqual(retrieved.value, 0.03)

    def test_update_assumption(self):
        assumption = ScenarioAssumption(name="tax_rate", value=0.20)
        self.manager.add_assumption(assumption)

        success = self.manager.update_assumption(assumption.name, 0.25)
        self.assertTrue(success)

        retrieved = self.manager.get_assumption(assumption.name)
        self.assertEqual(retrieved.value, 0.25)

    def test_remove_assumption(self):
        assumption = ScenarioAssumption(name="rent", value=5000)
        self.manager.add_assumption(assumption)

        success = self.manager.remove_assumption(assumption.name)
        self.assertTrue(success)

        self.assertIsNone(self.manager.get_assumption(assumption.name))

    def test_validate_assumptions_valid(self):
        self.manager.add_assumption(ScenarioAssumption(name="A", value=1))
        self.manager.add_assumption(ScenarioAssumption(name="B", value=2))
        self.assertTrue(self.manager.validate_assumptions())

    def test_validate_assumptions_invalid(self):
        self.manager.add_assumption(ScenarioAssumption(name="", value=1))
        with self.assertRaises(ValueError):
            self.manager.validate_assumptions()


if __name__ == "__main__":
    unittest.main()
