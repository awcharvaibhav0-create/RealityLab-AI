import unittest
from backend.services.coordinator.state_machine import WorkflowStateMachine
from backend.services.coordinator.models import WorkflowState


class TestStateMachine(unittest.TestCase):
    def test_transitions(self):
        sm = WorkflowStateMachine()
        self.assertEqual(sm.current_state, WorkflowState.CREATED)

        self.assertTrue(sm.transition_to(WorkflowState.RUNNING))
        self.assertEqual(sm.current_state, WorkflowState.RUNNING)

        self.assertTrue(sm.transition_to(WorkflowState.PAUSED))
        self.assertEqual(sm.current_state, WorkflowState.PAUSED)

        self.assertTrue(sm.transition_to(WorkflowState.RUNNING))

        self.assertFalse(sm.transition_to(WorkflowState.CREATED))

        self.assertTrue(sm.transition_to(WorkflowState.COMPLETED))
        self.assertEqual(sm.current_state, WorkflowState.COMPLETED)

        self.assertFalse(sm.transition_to(WorkflowState.RUNNING))


if __name__ == "__main__":
    unittest.main()
