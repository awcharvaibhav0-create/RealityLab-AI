from typing import Any
from .models import ReportData, ReportFormat
from .pdf_generator import PDFGenerator
from .html_generator import HTMLGenerator
from .markdown_generator import MarkdownGenerator
from .json_exporter import JSONExporter
from .csv_exporter import CSVExporter
from .validator import ReportValidator
from .config import ReportConfig


class ReportEngine:
    """Facade for generating reports in various formats."""

    def __init__(self, config: ReportConfig = None):
        self.config = config or ReportConfig()
        self.validator = ReportValidator()
        self.generators = {
            ReportFormat.PDF: PDFGenerator(),
            ReportFormat.HTML: HTMLGenerator(),
            ReportFormat.MARKDOWN: MarkdownGenerator(),
            ReportFormat.JSON: JSONExporter(),
            ReportFormat.CSV: CSVExporter(),
        }

    def generate(
        self, report_data: ReportData, format: ReportFormat = ReportFormat.PDF
    ) -> Any:
        self.validator.validate_report(report_data)
        generator = self.generators.get(format)
        if not generator:
            raise ValueError(f"Unsupported format: {format}")

        if hasattr(generator, "generate"):
            return generator.generate(report_data)
        elif hasattr(generator, "export"):
            return generator.export(report_data)
        else:
            raise NotImplementedError("Generator missing generate or export method")
