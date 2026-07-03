from .models import Evidence, ConfidenceLevel


class QualityAssessor:
    """Assesses the quality of evidence."""

    def assess_quality(self, evidence: Evidence) -> float:
        """
        Returns a quality score between 0.0 and 1.0.
        """
        score = 0.5
        if evidence.confidence == ConfidenceLevel.CERTAIN:
            score = 1.0
        elif evidence.confidence == ConfidenceLevel.HIGH:
            score = 0.8
        elif evidence.confidence == ConfidenceLevel.LOW:
            score = 0.2

        # Additional heuristics can be applied here based on metadata or content length
        if isinstance(evidence.content, str) and len(evidence.content) > 10:
            score = min(1.0, score + 0.1)

        return score
