import unittest
import time
from backend.services.coordinator.workflow_engine import WorkflowEngine
from backend.services.coordinator.event_bus import EventBus
from backend.services.coordinator.shared_context import SharedContext
from backend.services.coordinator.models import Task, TaskState, WorkflowState


class TestWorkflowEngine(unittest.TestCase):
    def test_engine_execution(self):
        bus = EventBus()
        ctx = SharedContext()
        engine = WorkflowEngine(bus, ctx)

        t1_run = False

        def action1():
            nonlocal t1_run
            t1_run = True

        t1 = Task(name="t1", action=action1)
        engine.add_task(t1)

        engine.start()
        time.sleep(0.2)

        self.assertTrue(t1_run)
        self.assertEqual(t1.state, TaskState.COMPLETED)
        self.assertEqual(engine.state_machine.current_state, WorkflowState.COMPLETED)


if __name__ == "__main__":
    unittest.main()
