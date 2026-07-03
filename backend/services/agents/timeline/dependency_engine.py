from typing import List
from .models import Task


class DependencyEngine:
    """Advanced dependency operations, like cycle detection."""

    def detect_cycles(self, tasks: List[Task]) -> bool:
        """
        Detects if there are cyclical dependencies in the task list.
        Returns True if a cycle is found, False otherwise.
        """
        adj = {t.id: [] for t in tasks}
        for t in tasks:
            for d in t.dependencies:
                # d.task_id must exist in adj
                if d.task_id in adj:
                    adj[d.task_id].append(t.id)

        visited = {t.id: False for t in tasks}
        rec_stack = {t.id: False for t in tasks}

        def is_cyclic(node):
            visited[node] = True
            rec_stack[node] = True

            for neighbor in adj[node]:
                if not visited[neighbor]:
                    if is_cyclic(neighbor):
                        return True
                elif rec_stack[neighbor]:
                    return True

            rec_stack[node] = False
            return False

        for node in visited:
            if not visited[node]:
                if is_cyclic(node):
                    return True

        return False
