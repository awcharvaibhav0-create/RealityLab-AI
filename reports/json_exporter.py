import json
from .models import ReportData


class JSONExporter:
    def export(self, report: ReportData) -> str:
        data = {
            "title": report.title,
            "author": report.author,
            "sections": [
                {"title": s.title, "content": s.content} for s in report.sections
            ],
        }
        return json.dumps(data, indent=2)
