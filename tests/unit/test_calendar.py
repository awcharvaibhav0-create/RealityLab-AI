import unittest
from datetime import date
from backend.services.agents.timeline.calendar_engine import CalendarEngine


class TestCalendarEngine(unittest.TestCase):
    def setUp(self):
        self.calendar = CalendarEngine(holidays=[date(2026, 1, 1)])

    def test_is_working_day(self):
        # Mon Jan 5 2026 is a weekday
        self.assertTrue(self.calendar.is_working_day(date(2026, 1, 5)))
        # Sat Jan 3 2026 is a weekend
        self.assertFalse(self.calendar.is_working_day(date(2026, 1, 3)))
        # Jan 1 is a holiday
        self.assertFalse(self.calendar.is_working_day(date(2026, 1, 1)))

    def test_add_working_days(self):
        # Jan 5 2026 (Mon) + 5 days = Jan 12 2026 (Mon)
        start = date(2026, 1, 5)
        end = self.calendar.add_working_days(start, 5)
        self.assertEqual(end, date(2026, 1, 12))


if __name__ == "__main__":
    unittest.main()
