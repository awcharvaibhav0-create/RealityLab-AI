import csv
import io
from .models import ReportData


class CSVExporter:
    def export(self, report: ReportData) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Section Title", "Content"])
        for section in report.sections:
            writer.writerow([section.title, section.content])
        return output.getvalue()
