from datetime import date, timedelta
from typing import List


class CalendarEngine:
    """Handles calendar operations, including skipping weekends and holidays."""

    def __init__(self, holidays: List[date] = None):
        self.holidays = holidays or []

    def add_working_days(self, start_date: date, days: int) -> date:
        """Adds a given number of working days to the start date."""
        current_date = start_date
        added_days = 0

        while added_days < days:
            current_date += timedelta(days=1)
            if self.is_working_day(current_date):
                added_days += 1

        return current_date

    def is_working_day(self, d: date) -> bool:
        """Returns True if the date is a working day (Mon-Fri, not a holiday)."""
        if d.weekday() >= 5:  # 5=Sat, 6=Sun
            return False
        if d in self.holidays:
            return False
        return True
