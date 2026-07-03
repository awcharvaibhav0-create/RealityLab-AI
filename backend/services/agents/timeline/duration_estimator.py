from .models import Task


class DurationEstimator:
    """Estimates durations for tasks based on complexity and historical data."""

    def estimate(self, task: Task, complexity: str = "medium") -> int:
        """
        Estimate duration based on complexity.
        Returns duration in days.
        """
        base_durations = {"low": 2, "medium": 5, "high": 10}

        return base_durations.get(complexity, 5)
