from .report_builder import ReportBuilder
from .models import ReportData


class RiskReport:
    @staticmethod
    def create(data: dict) -> ReportData:
        builder = ReportBuilder()
        builder.set_title("Risk Report")
        builder.set_author(data.get("author", "Unknown"))
        builder.add_section("Identified Risks", data.get("risks", ""), 1)
        builder.add_section("Mitigation Strategies", data.get("mitigations", ""), 2)
        return builder.build()
