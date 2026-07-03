import unittest
from backend.services.coordinator.scheduler import Scheduler
from backend.services.coordinator.models import Task, TaskState


class TestScheduler(unittest.TestCase):
    def test_dependencies(self):
        scheduler = Scheduler()

        t1 = Task(name="t1", action=lambda: None)
        t2 = Task(name="t2", action=lambda: None, dependencies=[t1.task_id])

        scheduler.add_task(t1)
        scheduler.add_task(t2)

        next_task = scheduler.get_next_task()
        self.assertEqual(next_task.task_id, t1.task_id)

        t1.state = TaskState.COMPLETED

        next_task = scheduler.get_next_task()
        self.assertEqual(next_task.task_id, t2.task_id)


if __name__ == "__main__":
    unittest.main()
