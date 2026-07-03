import threading
import logging
from .models import Task, TaskState, WorkflowState, Event
from .scheduler import Scheduler
from .shared_context import SharedContext
from .state_machine import WorkflowStateMachine
from .event_bus import EventBus

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """Executes tasks according to the scheduler and manages workflow state."""

    def __init__(self, event_bus: EventBus, shared_context: SharedContext):
        self.scheduler = Scheduler()
        self.state_machine = WorkflowStateMachine()
        self.event_bus = event_bus
        self.shared_context = shared_context
        self._stop_event = threading.Event()
        self._worker_thread = None

    def add_task(self, task: Task) -> None:
        """Add a task to the engine's scheduler."""
        self.scheduler.add_task(task)
        self.event_bus.publish(
            Event(topic="task.added", payload={"task_id": task.task_id})
        )

    def start(self) -> bool:
        """Start the execution loop."""
        if self.state_machine.transition_to(WorkflowState.RUNNING):
            self._stop_event.clear()
            self._worker_thread = threading.Thread(target=self._run_loop, daemon=True)
            self._worker_thread.start()
            self.event_bus.publish(Event(topic="workflow.started"))
            return True
        return False

    def stop(self) -> bool:
        """Pause the execution loop."""
        if self.state_machine.transition_to(WorkflowState.PAUSED):
            self._stop_event.set()
            if self._worker_thread:
                self._worker_thread.join(timeout=2.0)
            self.event_bus.publish(Event(topic="workflow.paused"))
            return True
        return False

    def _run_loop(self) -> None:
        while not self._stop_event.is_set():
            task = self.scheduler.get_next_task()
            if not task:
                all_tasks = self.scheduler.get_all_tasks()
                if not all_tasks:
                    # No tasks added, wait for tasks
                    self._stop_event.wait(0.1)
                    continue

                if all(
                    t.state
                    in (TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED)
                    for t in all_tasks
                ):
                    # Workflow is finished
                    if any(t.state == TaskState.FAILED for t in all_tasks):
                        self.state_machine.transition_to(WorkflowState.FAILED)
                        self.event_bus.publish(Event(topic="workflow.failed"))
                    else:
                        self.state_machine.transition_to(WorkflowState.COMPLETED)
                        self.event_bus.publish(Event(topic="workflow.completed"))
                    break

                # Dependencies not met yet, wait
                self._stop_event.wait(0.1)
                continue

            self._execute_task(task)

    def _execute_task(self, task: Task) -> None:
        task.state = TaskState.RUNNING
        self.event_bus.publish(
            Event(topic="task.started", payload={"task_id": task.task_id})
        )

        from .retry_manager import RetryManager

        retry_manager = RetryManager(
            max_retries=3, base_delay=0.1
        )  # Small delay for tests

        try:
            result = retry_manager.execute_with_retry(task.action, task.task_id)
            task.result = result
            task.state = TaskState.COMPLETED
            self.event_bus.publish(
                Event(
                    topic="task.completed",
                    payload={"task_id": task.task_id, "result": result},
                )
            )
        except Exception as e:
            logger.error(f"Task {task.task_id} failed finally: {e}")
            task.error = e
            task.state = TaskState.FAILED
            self.event_bus.publish(
                Event(
                    topic="task.failed",
                    payload={"task_id": task.task_id, "error": str(e)},
                )
            )
