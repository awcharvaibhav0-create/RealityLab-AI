from .models import ReportData


class HTMLGenerator:
    def generate(self, report: ReportData) -> str:
        html = f"<html><head><title>{report.title}</title></head><body>"
        html += f"<h1>{report.title}</h1><p>Author: {report.author}</p>"
        for section in sorted(report.sections, key=lambda s: s.order):
            html += f"<h2>{section.title}</h2><p>{section.content}</p>"
        html += "</body></html>"
        return html
