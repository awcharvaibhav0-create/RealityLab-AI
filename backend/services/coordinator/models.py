from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class TaskState(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class WorkflowState(Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class Event:
    topic: str
    payload: Dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Task:
    name: str
    action: Any
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    state: TaskState = TaskState.PENDING
    dependencies: List[str] = field(default_factory=list)
    result: Any = None
    error: Optional[Exception] = None
