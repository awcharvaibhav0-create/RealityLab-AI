from typing import Dict, List
from .models import WorkflowState
import threading


class WorkflowStateMachine:
    """State machine governing workflow lifecycle."""

    def __init__(self):
        self._state = WorkflowState.CREATED
        self._lock = threading.RLock()

        self._transitions: Dict[WorkflowState, List[WorkflowState]] = {
            WorkflowState.CREATED: [WorkflowState.RUNNING, WorkflowState.FAILED],
            WorkflowState.RUNNING: [
                WorkflowState.PAUSED,
                WorkflowState.COMPLETED,
                WorkflowState.FAILED,
            ],
            WorkflowState.PAUSED: [WorkflowState.RUNNING, WorkflowState.FAILED],
            WorkflowState.COMPLETED: [],
            WorkflowState.FAILED: [],
        }

    @property
    def current_state(self) -> WorkflowState:
        """Get the current state."""
        with self._lock:
            return self._state

    def transition_to(self, new_state: WorkflowState) -> bool:
        """Attempt to transition to a new state."""
        with self._lock:
            if new_state in self._transitions.get(self._state, []):
                self._state = new_state
                return True
            return False

    def can_transition(self, state: WorkflowState) -> bool:
        """Check if a transition is valid from the current state."""
        with self._lock:
            return state in self._transitions.get(self._state, [])
