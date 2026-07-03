from dataclasses import dataclass, field
from typing import Dict


@dataclass
class ConfidenceScore:
    """Represents a calculated confidence score."""

    value: float
    factors: Dict[str, float] = field(default_factory=dict)
