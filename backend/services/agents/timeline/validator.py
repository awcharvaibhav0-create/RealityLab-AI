from .models import Timeline
from .dependency_engine import DependencyEngine


class Validator:
    """Validates timeline integrity."""

    def __init__(self, dependency_engine: DependencyEngine):
        self.dependency_engine = dependency_engine

    def validate(self, timeline: Timeline) -> bool:
        """
        Validates the timeline structure.
        - Checks for cyclic dependencies.
        - Checks for valid dates.
        """
        all_tasks = []
        for phase in timeline.phases:
            all_tasks.extend(phase.tasks)

        if self.dependency_engine.detect_cycles(all_tasks):
            return False

        for t in all_tasks:
            if t.start_date and t.end_date and t.start_date > t.end_date:
                return False

        return True
