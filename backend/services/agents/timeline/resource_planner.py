from typing import List
from .models import Task, Resource


class ResourcePlanner:
    """Allocates resources to tasks."""

    def allocate(self, tasks: List[Task], resources: List[Resource]):
        """
        Assigns available resources to tasks based on some heuristics (e.g. role).
        For simplicity, assigns first available resource.
        """
        if not resources:
            return

        for t in tasks:
            if not t.resources:
                # Assign the first resource as default
                t.resources.append(resources[0].id)
