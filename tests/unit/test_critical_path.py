import unittest
from backend.services.agents.timeline.models import Task, Dependency
from backend.services.agents.timeline.critical_path import CriticalPath


class TestCriticalPath(unittest.TestCase):
    def setUp(self):
        self.cp = CriticalPath()

    def test_calculate_critical_path(self):
        t1 = Task(id="1", name="t1", description="", duration_days=5)
        t2 = Task(id="2", name="t2", description="", duration_days=10)
        t3 = Task(id="3", name="t3", description="", duration_days=2)

        # t2 depends on t1
        t2.dependencies.append(Dependency(task_id="1"))
        # t3 depends on t1
        t3.dependencies.append(Dependency(task_id="1"))

        path = self.cp.calculate([t1, t2, t3])
        # Longest path is t1 -> t2 (5 + 10 = 15)
        self.assertEqual(path, ["1", "2"])


if __name__ == "__main__":
    unittest.main()
