from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date


@dataclass
class Resource:
    id: str
    name: str
    role: str
    capacity: float = 1.0


@dataclass
class Dependency:
    task_id: str
    type: str = "FS"  # FS: Finish-to-Start


@dataclass
class Task:
    id: str
    name: str
    description: str
    duration_days: int
    dependencies: List[Dependency] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = "pending"


@dataclass
class Milestone:
    id: str
    name: str
    date: Optional[date] = None
    tasks: List[str] = field(default_factory=list)


@dataclass
class Phase:
    id: str
    name: str
    tasks: List[Task] = field(default_factory=list)
    milestones: List[Milestone] = field(default_factory=list)
    start_date: Optional[date] = None
    end_date: Optional[date] = None


@dataclass
class Timeline:
    id: str
    scenario_id: str
    phases: List[Phase] = field(default_factory=list)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    critical_path: List[str] = field(default_factory=list)
    confidence_score: float = 0.0


@dataclass
class TimelineResult:
    setup_phase_weeks: int
    breakeven_month: int
    milestones: List[str]
    critical_path: List[str]

    def to_dict(self):
        return {
            "setup_phase_weeks": self.setup_phase_weeks,
            "breakeven_month": self.breakeven_month,
            "milestones": self.milestones,
            "critical_path": self.critical_path,
        }
