from .report_builder import ReportBuilder
from .models import ReportData


class ExecutiveSummaryReport:
    @staticmethod
    def create(data: dict) -> ReportData:
        builder = ReportBuilder()
        builder.set_title("Executive Summary")
        builder.set_author(data.get("author", "Unknown"))
        builder.add_section("Overview", data.get("overview", ""), 1)
        builder.add_section("Key Findings", data.get("findings", ""), 2)
        return builder.build()
