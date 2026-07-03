from typing import List, Optional
from datetime import date
import uuid
from .models import Milestone


class MilestoneManager:
    """Manages creation and updates of milestones."""

    def create_milestone(
        self, name: str, date: Optional[date] = None, tasks: List[str] = None
    ) -> Milestone:
        """Creates a new milestone."""
        return Milestone(id=str(uuid.uuid4()), name=name, date=date, tasks=tasks or [])
