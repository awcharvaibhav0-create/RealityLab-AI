from typing import List
from .models import Evidence
from .quality import QualityAssessor


class EvidenceRanker:
    """Ranks evidence based on quality and relevance."""

    def __init__(self, quality_assessor: QualityAssessor):
        self.quality_assessor = quality_assessor

    def rank_evidence(self, evidences: List[Evidence]) -> List[Evidence]:
        """
        Sorts evidence by quality score in descending order.
        """

        def get_score(evidence: Evidence) -> float:
            return self.quality_assessor.assess_quality(evidence)

        return sorted(evidences, key=get_score, reverse=True)
