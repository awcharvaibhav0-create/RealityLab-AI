from .models import Evidence


class EvidenceValidator:
    """Validates that evidence meets certain criteria before being processed."""

    def validate(self, evidence: Evidence) -> bool:
        """
        Validates the given evidence.
        """
        if not evidence.content:
            return False
        if not evidence.evidence_id or not evidence.source:
            return False
        return True
