from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


class ScenarioStatus(Enum):
    PENDING = "PENDING"
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ABORTED = "ABORTED"


class AssumptionPriority(Enum):
    USER_OVERRIDE = 1
    HISTORICAL_DATA = 2
    BUSINESS_RULES = 3
    INDUSTRY_DEFAULT = 4
    GLOBAL_DEFAULT = 5


@dataclass
class ScenarioAssumption:
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    value: Any = None
    reason: str = ""
    source: str = ""
    confidence: str = "Medium"
    version: str = "1.0"
    priority: AssumptionPriority = AssumptionPriority.GLOBAL_DEFAULT
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResourceAllocation:
    cpu_cores: float = 1.0
    memory_mb: float = 1024.0
    gpu_count: int = 0
    timeout_seconds: int = 3600


@dataclass
class ScenarioContext:
    id: UUID = field(default_factory=uuid4)
    variables: Dict[str, Any] = field(default_factory=dict)
    state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScenarioConfig:
    name: str
    description: str = ""
    base_context: Optional[ScenarioContext] = None
    assumptions: List[ScenarioAssumption] = field(default_factory=list)
    resources: ResourceAllocation = field(default_factory=ResourceAllocation)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulationResult:
    scenario_id: UUID
    status: ScenarioStatus
    output_state: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)
    error_message: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


@dataclass
class Scenario:
    id: UUID = field(default_factory=uuid4)
    config: ScenarioConfig = field(
        default_factory=lambda: ScenarioConfig(name="Default")
    )
    context: ScenarioContext = field(default_factory=ScenarioContext)
    status: ScenarioStatus = ScenarioStatus.PENDING
    result: Optional[SimulationResult] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
