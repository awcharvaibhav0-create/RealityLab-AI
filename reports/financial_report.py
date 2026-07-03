from .report_builder import ReportBuilder
from .models import ReportData


class FinancialReport:
    @staticmethod
    def create(data: dict) -> ReportData:
        builder = ReportBuilder()
        builder.set_title("Financial Report")
        builder.set_author(data.get("author", "Unknown"))
        builder.add_section("Revenue", data.get("revenue", ""), 1)
        builder.add_section("Expenses", data.get("expenses", ""), 2)
        return builder.build()
