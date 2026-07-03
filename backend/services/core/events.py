from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4, UUID
from typing import Optional
from .types import PayloadType
from .constants import EventPriority


@dataclass
class Event:
    """Represents a discrete event in the system."""

    name: str
    payload: PayloadType = field(default_factory=dict)
    priority: EventPriority = EventPriority.NORMAL
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source: Optional[str] = None
