import unittest
from datetime import date
from backend.services.agents.timeline.timeline_agent import TimelineAgent
from backend.services.agents.timeline.planner import Planner
from backend.services.agents.timeline.task_generator import TaskGenerator
from backend.services.agents.timeline.phase_builder import PhaseBuilder
from backend.services.agents.timeline.timeline_engine import TimelineEngine
from backend.services.agents.timeline.resource_planner import ResourcePlanner
from backend.services.agents.timeline.milestone_engine import MilestoneEngine
from backend.services.agents.timeline.confidence_engine import ConfidenceEngine
from backend.services.agents.timeline.calendar_engine import CalendarEngine
from backend.services.agents.timeline.critical_path import CriticalPath
from backend.services.agents.timeline.dependency_engine import DependencyEngine
from backend.services.agents.timeline.validator import Validator


class TestTimelineAgent(unittest.TestCase):
    def setUp(self):
        cal = CalendarEngine()
        cp = CriticalPath()
        dep = DependencyEngine()

        planner = Planner(
            task_generator=TaskGenerator(),
            phase_builder=PhaseBuilder(),
            timeline_engine=TimelineEngine(cal, cp),
            resource_planner=ResourcePlanner(),
            milestone_engine=MilestoneEngine(),
            confidence_engine=ConfidenceEngine(),
        )
        validator = Validator(dep)
        self.agent = TimelineAgent(planner, validator)

    def test_generate_timeline(self):
        start = date(2026, 1, 1)
        timeline = self.agent.generate_timeline("scen1", start)

        self.assertIsNotNone(timeline)
        self.assertEqual(timeline["timeline"].scenario_id, "scen1")
        self.assertEqual(timeline["timeline"].start_date, start)
        self.assertTrue(len(timeline["timeline"].phases) > 0)

        # Verify tasks have dates
        all_tasks = [t for p in timeline["timeline"].phases for t in p.tasks]
        self.assertTrue(all(t.start_date is not None for t in all_tasks))
        self.assertTrue(all(t.end_date is not None for t in all_tasks))


if __name__ == "__main__":
    unittest.main()
