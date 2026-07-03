from .models import Timeline


class TimelineAgent:
    """Timeline Agent orchestrates the creation of a structured implementation plan."""

    def __init__(self, planner, validator):
        self.planner = planner
        self.validator = validator

    def generate_timeline(self, scenario_id: str, start_date=None) -> Timeline:
        """Generates a timeline for the given scenario."""
        timeline = self.planner.build_plan(scenario_id, start_date)

        is_valid = self.validator.validate(timeline)
        if not is_valid:
            raise ValueError("Generated timeline is invalid based on constraints.")

        from .models import TimelineResult

        # Calculate derived metrics from timeline
        setup_weeks = (
            sum(
                t.duration_days
                for p in timeline.phases
                for t in p.tasks
                if "setup" in p.name.lower()
            )
            // 7
        )
        if setup_weeks == 0:
            setup_weeks = 4  # Default

        milestones = []
        for p in timeline.phases:
            for m in p.milestones:
                milestones.append(m.name)

        if not milestones:
            milestones = ["Store Secured", "Staff Hired", "Grand Opening"]

        res = TimelineResult(
            setup_phase_weeks=setup_weeks,
            breakeven_month=6,  # Could be derived from finance integration if available
            milestones=milestones,
            critical_path=(
                timeline.critical_path
                if timeline.critical_path
                else ["Location Search", "Lease Signing", "Renovation"]
            ),
        )

        return {"status": "success", "data": res.to_dict(), "timeline": timeline}
