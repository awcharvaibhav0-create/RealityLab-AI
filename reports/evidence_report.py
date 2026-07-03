from .report_builder import ReportBuilder
from .models import ReportData


class EvidenceReport:
    @staticmethod
    def create(data: dict) -> ReportData:
        builder = ReportBuilder()
        builder.set_title("Evidence Report")
        builder.set_author(data.get("author", "Unknown"))
        builder.add_section("Sources", data.get("sources", ""), 1)
        builder.add_section("Data Points", data.get("data_points", ""), 2)
        return builder.build()
