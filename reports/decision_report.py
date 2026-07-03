from .report_builder import ReportBuilder
from .models import ReportData


class DecisionReport:
    @staticmethod
    def create(data: dict) -> ReportData:
        builder = ReportBuilder()
        builder.set_title("Decision Report")
        builder.set_author(data.get("author", "Unknown"))
        builder.add_section("Context", data.get("context", ""), 1)
        builder.add_section("Options & Conclusion", data.get("options", ""), 2)
        return builder.build()
