import unittest
from backend.services.agents.timeline.models import Task, Dependency
from backend.services.agents.timeline.dependency_engine import DependencyEngine


class TestDependencyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DependencyEngine()

    def test_detect_cycles_no_cycle(self):
        t1 = Task(id="1", name="t1", description="", duration_days=1)
        t2 = Task(id="2", name="t2", description="", duration_days=1)
        t2.dependencies.append(Dependency(task_id="1"))

        self.assertFalse(self.engine.detect_cycles([t1, t2]))

    def test_detect_cycles_with_cycle(self):
        t1 = Task(id="1", name="t1", description="", duration_days=1)
        t2 = Task(id="2", name="t2", description="", duration_days=1)
        t1.dependencies.append(Dependency(task_id="2"))
        t2.dependencies.append(Dependency(task_id="1"))

        self.assertTrue(self.engine.detect_cycles([t1, t2]))


if __name__ == "__main__":
    unittest.main()
