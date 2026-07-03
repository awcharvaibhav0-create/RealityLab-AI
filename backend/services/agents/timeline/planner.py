from datetime import date
import uuid
from .models import Timeline, Resource
from .task_generator import TaskGenerator
from .phase_builder import PhaseBuilder
from .timeline_engine import TimelineEngine
from .resource_planner import ResourcePlanner
from .milestone_engine import MilestoneEngine
from .confidence_engine import ConfidenceEngine


class Planner:
    """Orchestrates building a full timeline."""

    def __init__(
        self,
        task_generator: TaskGenerator,
        phase_builder: PhaseBuilder,
        timeline_engine: TimelineEngine,
        resource_planner: ResourcePlanner,
        milestone_engine: MilestoneEngine,
        confidence_engine: ConfidenceEngine,
    ):
        self.task_generator = task_generator
        self.phase_builder = phase_builder
        self.timeline_engine = timeline_engine
        self.resource_planner = resource_planner
        self.milestone_engine = milestone_engine
        self.confidence_engine = confidence_engine

    def build_plan(self, scenario_id: str, start_date: date = None) -> Timeline:
        """Builds a comprehensive timeline plan."""
        if start_date is None:
            start_date = date.today()

        timeline = Timeline(id=str(uuid.uuid4()), scenario_id=scenario_id)

        # 1. Generate tasks
        tasks = self.task_generator.generate_tasks(scenario_id)

        # 2. Build phases
        timeline.phases = self.phase_builder.build_phases(tasks)

        # 3. Resource allocation (mock)
        resources = [
            Resource(id="r1", name="Alice", role="Developer"),
            Resource(id="r2", name="Bob", role="Designer"),
        ]
        self.resource_planner.allocate(tasks, resources)

        # 4. Schedule timeline
        self.timeline_engine.schedule(timeline, start_date)

        # 5. Evaluate milestones
        self.milestone_engine.evaluate_milestones(timeline)

        # 6. Calculate confidence
        timeline.confidence_score = self.confidence_engine.evaluate(timeline)

        return timeline
