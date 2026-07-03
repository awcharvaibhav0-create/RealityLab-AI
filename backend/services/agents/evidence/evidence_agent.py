from typing import List, Any
from .models import Evidence, EvidenceSource, EvidenceType, ConfidenceLevel
from .evidence_engine import EvidenceEngine


class EvidenceAgent:
    """
    Evidence Agent that interfaces with other agents in the RealityLab AI project.
    Collects, validates, ranks, and organizes evidence.
    """

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.engine = EvidenceEngine()

    def receive_evidence(
        self,
        content: Any,
        source_agent: str,
        evidence_id: str,
        evidence_type: EvidenceType = EvidenceType.FACT,
        confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM,
    ) -> bool:
        """
        Receives evidence from another agent and processes it.
        """
        source = EvidenceSource(
            source_id=f"src_{source_agent}", agent_name=source_agent
        )
        evidence = Evidence(
            evidence_id=evidence_id,
            content=content,
            source=source,
            evidence_type=evidence_type,
            confidence=confidence,
        )
        return self.engine.process_new_evidence(evidence)

    def analyze_current_state(self) -> dict:
        """
        Analyzes the current evidence state and returns a summary including conflicts.
        """
        conflicts = self.engine.get_conflicts()
        report = self.engine.generate_report()

        return {
            "evidence_count": len(self.engine.collector.get_all_evidence()),
            "conflict_count": len(conflicts),
            "report": report,
        }

    def get_best_evidence(self) -> List[Evidence]:
        """Returns evidence ranked by quality."""
        return self.engine.get_processed_evidence()
