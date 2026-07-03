from datetime import date
from .models import Timeline
from .calendar_engine import CalendarEngine
from .critical_path import CriticalPath


class TimelineEngine:
    """Calculates start and end dates for all tasks."""

    def __init__(self, calendar_engine: CalendarEngine, critical_path: CriticalPath):
        self.calendar = calendar_engine
        self.critical_path = critical_path

    def schedule(self, timeline: Timeline, start_date: date):
        """Schedules all tasks in the timeline."""
        timeline.start_date = start_date

        all_tasks = []
        for phase in timeline.phases:
            all_tasks.extend(phase.tasks)

        # Simplistic topological sort for scheduling
        task_dict = {t.id: t for t in all_tasks}
        in_degree = {t.id: 0 for t in all_tasks}
        adj = {t.id: [] for t in all_tasks}

        for t in all_tasks:
            for d in t.dependencies:
                if d.task_id in adj:
                    adj[d.task_id].append(t.id)
                    in_degree[t.id] += 1

        import collections

        queue = collections.deque([t.id for t in all_tasks if in_degree[t.id] == 0])

        for tid in queue:
            t = task_dict[tid]
            t.start_date = start_date
            t.end_date = self.calendar.add_working_days(t.start_date, t.duration_days)

        topo_order = []
        while queue:
            u = queue.popleft()
            topo_order.append(u)

            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

                t_u = task_dict[u]
                t_v = task_dict[v]

                # FS dependency: v starts after u ends
                if not t_v.start_date or t_v.start_date < t_u.end_date:
                    t_v.start_date = t_u.end_date
                    t_v.end_date = self.calendar.add_working_days(
                        t_v.start_date, t_v.duration_days
                    )

        # Update timeline end_date
        if all_tasks:
            timeline.end_date = max(t.end_date for t in all_tasks if t.end_date)

        # Calculate critical path
        timeline.critical_path = self.critical_path.calculate(all_tasks)
