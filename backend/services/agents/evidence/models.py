from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class EvidenceType(Enum):
    FACT = "fact"
    OPINION = "opinion"
    INFERENCE = "inference"
    CODE_SNIPPET = "code_snippet"


class ConfidenceLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CERTAIN = 4


@dataclass
class EvidenceSource:
    source_id: str
    agent_name: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Evidence:
    evidence_id: str
    content: Any
    source: EvidenceSource
    evidence_type: EvidenceType = EvidenceType.FACT
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Assumption:
    assumption_id: str
    description: str
    related_evidence_ids: List[str] = field(default_factory=list)
    is_verified: bool = False


@dataclass
class Conflict:
    conflict_id: str
    description: str
    evidence_ids: List[str]
    resolved: bool = False
    resolution_notes: Optional[str] = None
