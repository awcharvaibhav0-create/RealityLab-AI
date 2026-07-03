from typing import List
import uuid
from .models import Task, Dependency


class TaskGenerator:
    """Generates tasks based on scenario."""

    def generate_tasks(self, scenario_id: str) -> List[Task]:
        """
        Generates a set of tasks for a given scenario.
        For now, returns some sample tasks.
        """
        t1 = Task(
            id=str(uuid.uuid4()),
            name="Requirements Gathering",
            description="Gather reqs",
            duration_days=5,
        )
        t2 = Task(
            id=str(uuid.uuid4()),
            name="System Design",
            description="Design arch",
            duration_days=7,
        )
        t3 = Task(
            id=str(uuid.uuid4()),
            name="Implementation",
            description="Write code",
            duration_days=14,
        )
        t4 = Task(
            id=str(uuid.uuid4()),
            name="Testing",
            description="Run tests",
            duration_days=5,
        )

        # Add basic FS dependencies
        t2.dependencies.append(Dependency(task_id=t1.id))
        t3.dependencies.append(Dependency(task_id=t2.id))
        t4.dependencies.append(Dependency(task_id=t3.id))

        return [t1, t2, t3, t4]
