from typing import List
from .models import Task


class CriticalPath:
    """Calculates the critical path of a timeline."""

    def calculate(self, tasks: List[Task]) -> List[str]:
        """
        Determines the longest path in the dependency network.
        Returns a list of task IDs on the critical path.
        """
        # A simplified topological sort and longest path algorithm
        adj = {t.id: [] for t in tasks}
        in_degree = {t.id: 0 for t in tasks}
        duration = {t.id: t.duration_days for t in tasks}

        for t in tasks:
            for dep in t.dependencies:
                if dep.task_id in adj:
                    adj[dep.task_id].append(t.id)
                    in_degree[t.id] += 1

        import collections

        queue = collections.deque([t.id for t in tasks if in_degree[t.id] == 0])
        dist = {t.id: duration[t.id] for t in tasks if in_degree[t.id] == 0}
        prev = {t.id: None for t in tasks}

        # For tasks not in queue initially, set distance to 0
        for t in tasks:
            if t.id not in dist:
                dist[t.id] = 0

        topo_order = []
        while queue:
            u = queue.popleft()
            topo_order.append(u)
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

                # Update longest path
                if dist[v] < dist[u] + duration[v]:
                    dist[v] = dist[u] + duration[v]
                    prev[v] = u

        if not dist:
            return []

        # Find the node with max distance
        max_node = max(dist, key=dist.get)

        # Backtrack to find path
        path = []
        curr = max_node
        while curr is not None:
            path.append(curr)
            curr = prev[curr]

        path.reverse()
        return path
