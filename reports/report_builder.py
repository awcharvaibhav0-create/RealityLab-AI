from .models import ReportData, ReportSection


class ReportBuilder:
    def __init__(self):
        self.report = ReportData(title="", author="")

    def set_title(self, title: str) -> "ReportBuilder":
        self.report.title = title
        return self

    def set_author(self, author: str) -> "ReportBuilder":
        self.report.author = author
        return self

    def add_section(self, title: str, content: str, order: int = 0) -> "ReportBuilder":
        self.report.sections.append(
            ReportSection(title=title, content=content, order=order)
        )
        return self

    def build(self) -> ReportData:
        return self.report
