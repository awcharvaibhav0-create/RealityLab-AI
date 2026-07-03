from .models import ReportData


class ReportValidator:
    @staticmethod
    def validate_report(report: ReportData) -> bool:
        if not report.title:
            raise ValueError("Report must have a title")
        if not report.sections:
            raise ValueError("Report must have at least one section")
        return True
