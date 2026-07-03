from typing import List
import uuid
from .models import Task, Phase


class PhaseBuilder:
    """Builds phases and assigns tasks to them."""

    def build_phases(self, tasks: List[Task]) -> List[Phase]:
        """
        Groups tasks into logical phases.
        For simplicity, groups first half of tasks in Phase 1, rest in Phase 2.
        """
        if not tasks:
            return []

        mid = max(1, len(tasks) // 2)

        phase1 = Phase(id=str(uuid.uuid4()), name="Planning & Design")
        phase1.tasks = tasks[:mid]

        phase2 = Phase(id=str(uuid.uuid4()), name="Execution & Delivery")
        phase2.tasks = tasks[mid:]

        return [phase1, phase2]
