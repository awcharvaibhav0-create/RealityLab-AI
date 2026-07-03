import unittest
import time
from backend.services.coordinator.coordinator import Coordinator
from backend.services.coordinator.models import WorkflowState, TaskState


class TestCoordinator(unittest.TestCase):
    def test_coordinator_execution(self):
        coord = Coordinator()

        task1_run = False
        task2_run = False

        def action1():
            nonlocal task1_run
            task1_run = True
            return "res1"

        def action2():
            nonlocal task2_run
            task2_run = True
            return "res2"

        t1 = coord.add_task("task1", action1)
        t2 = coord.add_task("task2", action2, dependencies=[t1.task_id])

        coord.execute()

        # wait a bit for thread to finish
        time.sleep(0.2)

        self.assertTrue(task1_run)
        self.assertTrue(task2_run)
        self.assertEqual(t1.state, TaskState.COMPLETED)
        self.assertEqual(t2.state, TaskState.COMPLETED)

        status = coord.monitor()
        self.assertEqual(status["workflow_state"], WorkflowState.COMPLETED.name)


if __name__ == "__main__":
    unittest.main()
