import unittest
from backend.services.agents.decision_score.models import ScenarioOutput
from backend.services.agents.decision_score.decision_score_agent import (
    DecisionScoreAgent,
)


class TestDecisionScoreEngine(unittest.TestCase):
    def setUp(self):
        self.agent = DecisionScoreAgent()
        self.scenarios = [
            ScenarioOutput(
                scenario_id="s1",
                strategy_id="strat_a",
                metrics={"profit": 100, "risk": 20},
                confidence=0.9,
            ),
            ScenarioOutput(
                scenario_id="s2",
                strategy_id="strat_a",
                metrics={"profit": 110, "risk": 25},
                confidence=0.8,
            ),
            ScenarioOutput(
                scenario_id="s3",
                strategy_id="strat_b",
                metrics={"profit": 150, "risk": 80},
                confidence=0.9,
            ),
        ]
        self.weights = {"profit": 0.8, "risk": -0.2}

    def test_evaluate_scenarios(self):
        recommendation = self.agent.process_scenarios(self.scenarios, self.weights)
        self.assertIsNotNone(recommendation)
        self.assertTrue(len(recommendation.rankings) > 0)

    def test_validator_fails_empty(self):
        with self.assertRaises(ValueError):
            self.agent.process_scenarios([], self.weights)


if __name__ == "__main__":
    unittest.main()
