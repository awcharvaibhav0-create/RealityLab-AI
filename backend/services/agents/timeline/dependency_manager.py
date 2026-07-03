from typing import List
from .models import Task, Dependency


class DependencyManager:
    """Manages dependencies for tasks."""

    def add_dependency(self, task: Task, dependency_id: str, dep_type: str = "FS"):
        """Adds a dependency to a task."""
        # Check if already exists
        for d in task.dependencies:
            if d.task_id == dependency_id:
                return
        task.dependencies.append(Dependency(task_id=dependency_id, type=dep_type))

    def remove_dependency(self, task: Task, dependency_id: str):
        """Removes a dependency from a task."""
        task.dependencies = [d for d in task.dependencies if d.task_id != dependency_id]

    def get_dependencies(self, task: Task) -> List[Dependency]:
        """Returns all dependencies of a task."""
        return task.dependencies
