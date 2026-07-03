from dataclasses import dataclass, field
from typing import List, Dict, Any
import time

@dataclass
class TraceStep:
    step_id: str
    action: str
    context: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

class DecisionTrace:
    """Records the steps taken by engines to reach a decision."""
    def __init__(self):
        self.steps: List[TraceStep] = []

    def add_step(self, step_id: str, action: str, context: Dict[str, Any]):
        self.steps.append(TraceStep(step_id, action, context))

    def get_trace(self) -> List[TraceStep]:
        return self.steps