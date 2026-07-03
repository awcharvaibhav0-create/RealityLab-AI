import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from reports.report_engine import ReportEngine
from reports.models import ReportData, ReportSection, ReportFormat


class TestReportEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ReportEngine()
        self.report_data = ReportData(
            title="Test Report",
            author="Tester",
            sections=[ReportSection(title="Intro", content="Hello World")],
        )

    def test_generate_markdown(self):
        result = self.engine.generate(self.report_data, ReportFormat.MARKDOWN)
        self.assertIn("# Test Report", result)
        self.assertIn("## Intro", result)

    def test_generate_json(self):
        result = self.engine.generate(self.report_data, ReportFormat.JSON)
        self.assertIn('"title": "Test Report"', result)

    def test_generate_invalid_report(self):
        invalid_data = ReportData(title="", author="", sections=[])
        with self.assertRaises(ValueError):
            self.engine.generate(invalid_data)


if __name__ == "__main__":
    unittest.main()
