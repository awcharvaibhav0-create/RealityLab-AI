from .models import Timeline


class MilestoneEngine:
    """Calculates milestone dates based on tasks."""

    def evaluate_milestones(self, timeline: Timeline):
        """
        Calculates or updates milestone dates.
        A milestone date could be the max end_date of its associated tasks.
        """
        task_end_dates = {}
        for phase in timeline.phases:
            for t in phase.tasks:
                if t.end_date:
                    task_end_dates[t.id] = t.end_date

        for phase in timeline.phases:
            for m in phase.milestones:
                if m.tasks:
                    dates = [
                        task_end_dates.get(tid)
                        for tid in m.tasks
                        if task_end_dates.get(tid)
                    ]
                    if dates:
                        m.date = max(dates)
