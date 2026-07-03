from typing import List
from .models import Evidence, Conflict
from .collector import EvidenceCollector
from .validator import EvidenceValidator
from .quality import QualityAssessor
from .conflict_detector import ConflictDetector
from .assumption_tracker import AssumptionTracker
from .ranker import EvidenceRanker
from .formatter import EvidenceFormatter


class EvidenceEngine:
    """Core engine orchestrating the evidence components."""

    def __init__(self):
        self.collector = EvidenceCollector()
        self.validator = EvidenceValidator()
        self.quality_assessor = QualityAssessor()
        self.conflict_detector = ConflictDetector()
        self.assumption_tracker = AssumptionTracker()
        self.ranker = EvidenceRanker(self.quality_assessor)
        self.formatter = EvidenceFormatter()

    def process_new_evidence(self, evidence: Evidence) -> bool:
        """Validates and collects new evidence."""
        if self.validator.validate(evidence):
            self.collector.add_evidence(evidence)
            return True
        return False

    def get_processed_evidence(self) -> List[Evidence]:
        """Retrieves and ranks all valid evidence."""
        evidences = self.collector.get_all_evidence()
        return self.ranker.rank_evidence(evidences)

    def get_conflicts(self) -> List[Conflict]:
        """Checks for conflicts in current evidence."""
        evidences = self.collector.get_all_evidence()
        return self.conflict_detector.detect_conflicts(evidences)

    def generate_report(self) -> str:
        """Generates a text report of current ranked evidence."""
        ranked = self.get_processed_evidence()
        return self.formatter.format_as_text(ranked)
