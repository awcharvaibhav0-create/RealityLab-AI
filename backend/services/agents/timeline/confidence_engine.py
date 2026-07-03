from .models import Timeline


class ConfidenceEngine:
    """Calculates confidence score for a timeline."""

    def evaluate(self, timeline: Timeline) -> float:
        """
        Calculates confidence score (0.0 to 1.0) based on factors like:
        - Density of critical path
        - Unresolved dependencies
        - Resource overallocation
        For now, returns a baseline score.
        """
        score = 0.85

        total_tasks = sum(len(phase.tasks) for phase in timeline.phases)
        if total_tasks == 0:
            return 0.0

        # Penalize if critical path involves too many tasks
        cp_ratio = len(timeline.critical_path) / total_tasks
        if cp_ratio > 0.8:
            score -= 0.2

        return max(0.0, min(1.0, score))
