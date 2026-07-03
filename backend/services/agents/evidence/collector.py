from typing import List, Dict
from .models import Evidence


class EvidenceCollector:
    """Collects evidence from various sources and agents."""

    def __init__(self):
        self.evidence_store: Dict[str, Evidence] = {}

    def add_evidence(self, evidence: Evidence) -> None:
        """Adds a piece of evidence to the store."""
        self.evidence_store[evidence.evidence_id] = evidence

    def get_all_evidence(self) -> List[Evidence]:
        """Retrieves all collected evidence."""
        return list(self.evidence_store.values())

    def get_evidence_by_agent(self, agent_name: str) -> List[Evidence]:
        """Retrieves evidence provided by a specific agent."""
        return [
            ev
            for ev in self.evidence_store.values()
            if ev.source.agent_name == agent_name
        ]

    def clear(self) -> None:
        """Clears all collected evidence."""
        self.evidence_store.clear()
