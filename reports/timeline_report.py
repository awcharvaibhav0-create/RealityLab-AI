from .report_builder import ReportBuilder
from .models import ReportData


class TimelineReport:
    @staticmethod
    def create(data: dict) -> ReportData:
        builder = ReportBuilder()
        builder.set_title("Timeline Report")
        builder.set_author(data.get("author", "Unknown"))
        builder.add_section("Milestones", data.get("milestones", ""), 1)
        builder.add_section("Schedule", data.get("schedule", ""), 2)
        return builder.build()
