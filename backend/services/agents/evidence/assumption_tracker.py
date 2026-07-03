from typing import List, Dict
from .models import Assumption


class AssumptionTracker:
    """Tracks assumptions made during evidence processing."""

    def __init__(self):
        self.assumptions: Dict[str, Assumption] = {}

    def add_assumption(self, assumption: Assumption) -> None:
        self.assumptions[assumption.assumption_id] = assumption

    def verify_assumption(self, assumption_id: str, verified: bool = True) -> None:
        if assumption_id in self.assumptions:
            self.assumptions[assumption_id].is_verified = verified

    def get_unverified_assumptions(self) -> List[Assumption]:
        return [a for a in self.assumptions.values() if not a.is_verified]

    def get_all_assumptions(self) -> List[Assumption]:
        return list(self.assumptions.values())
