import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from reports.report_builder import ReportBuilder
from reports.executive_summary import ExecutiveSummaryReport


class TestReportBuilder(unittest.TestCase):
    def test_build_report(self):
        builder = ReportBuilder()
        report = (
            builder.set_title("Built Title")
            .set_author("AuthorName")
            .add_section("S1", "C1")
            .build()
        )
        self.assertEqual(report.title, "Built Title")
        self.assertEqual(len(report.sections), 1)

    def test_executive_summary(self):
        data = {"author": "Jane", "overview": "Everything is fine."}
        report = ExecutiveSummaryReport.create(data)
        self.assertEqual(report.title, "Executive Summary")
        self.assertEqual(report.sections[0].title, "Overview")


if __name__ == "__main__":
    unittest.main()
