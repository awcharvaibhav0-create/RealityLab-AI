from .report_builder import ReportBuilder
from .models import ReportData


class MarketReport:
    @staticmethod
    def create(data: dict) -> ReportData:
        builder = ReportBuilder()
        builder.set_title("Market Report")
        builder.set_author(data.get("author", "Unknown"))
        builder.add_section("Market Trends", data.get("trends", ""), 1)
        builder.add_section("Competitor Analysis", data.get("competitors", ""), 2)
        return builder.build()
