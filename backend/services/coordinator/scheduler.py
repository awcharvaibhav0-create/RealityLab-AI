from typing import List, Optional
from .models import Task, TaskState
import threading


class Scheduler:
    """Manages tasks and determines the next task to run based on dependencies."""

    def __init__(self):
        self._tasks: List[Task] = []
        self._lock = threading.RLock()

    def add_task(self, task: Task) -> None:
        """Add a new task to the scheduler."""
        with self._lock:
            self._tasks.append(task)

    def get_next_task(self) -> Optional[Task]:
        """Find the next pending task whose dependencies are satisfied."""
        with self._lock:
            for task in self._tasks:
                if task.state == TaskState.PENDING:
                    deps_met = all(
                        any(
                            t.task_id == dep and t.state == TaskState.COMPLETED
                            for t in self._tasks
                        )
                        for dep in task.dependencies
                    )
                    if deps_met:
                        return task
            return None

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID."""
        with self._lock:
            for t in self._tasks:
                if t.task_id == task_id:
                    return t
            return None

    def get_all_tasks(self) -> List[Task]:
        """Return a copy of all tasks."""
        with self._lock:
            return list(self._tasks)
