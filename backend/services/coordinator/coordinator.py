from typing import Any, Callable, Dict, List, Optional
import logging
from .models import Task, Event
from .event_bus import EventBus
from .shared_context import SharedContext
from .workflow_engine import WorkflowEngine

logger = logging.getLogger(__name__)


class Coordinator:
    """Central orchestrator for the AI project."""

    def __init__(self):
        self.event_bus = EventBus()
        self.shared_context = SharedContext()
        self.workflow_engine = WorkflowEngine(self.event_bus, self.shared_context)

        self.event_bus.subscribe("*", self._on_event)
        self._event_history: List[Event] = []

    def _on_event(self, event: Event) -> None:
        self._event_history.append(event)
        logger.debug(f"Coordinator observed event: {event.topic} - {event.payload}")

    def add_task(
        self,
        name: str,
        action: Callable[[], Any],
        dependencies: Optional[List[str]] = None,
    ) -> Task:
        """Create and add a task to the workflow engine."""
        task = Task(name=name, action=action, dependencies=dependencies or [])
        self.workflow_engine.add_task(task)
        return task

    def start(self) -> bool:
        """Start the execution of the workflow."""
        return self.workflow_engine.start()

    def stop(self) -> bool:
        """Pause or stop the execution of the workflow."""
        return self.workflow_engine.stop()

    def execute(self, tasks: Optional[List[Task]] = None) -> None:
        """Convenience method to add tasks and start the engine."""
        if tasks:
            for t in tasks:
                self.workflow_engine.add_task(t)
        self.start()

    def monitor(self) -> Dict[str, Any]:
        """Return a snapshot of the current state of the workflow and its tasks."""
        tasks = self.workflow_engine.scheduler.get_all_tasks()
        return {
            "workflow_state": self.workflow_engine.state_machine.current_state.name,
            "tasks": [
                {
                    "task_id": t.task_id,
                    "name": t.name,
                    "state": t.state.name,
                    "dependencies": t.dependencies,
                }
                for t in tasks
            ],
            "event_count": len(self._event_history),
        }
