from .report_builder import ReportBuilder
from .models import ReportData


class ComparisonReport:
    @staticmethod
    def create(data: dict) -> ReportData:
        builder = ReportBuilder()
        builder.set_title("Comparison Report")
        builder.set_author(data.get("author", "Unknown"))
        builder.add_section("Entities", data.get("entities", ""), 1)
        builder.add_section("Differences", data.get("differences", ""), 2)
        return builder.build()
