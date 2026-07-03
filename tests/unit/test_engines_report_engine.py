import unittest
import json
from backend.services.engines.report.report_engine import ReportEngine


class TestEnginesReportEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ReportEngine()
        self.data = {"status": "success", "score": 95}

    def test_generate_json(self):
        result = self.engine.generate_json(self.data)
        self.assertIsInstance(result, bytes)
        parsed = json.loads(result.decode("utf-8"))
        self.assertEqual(parsed["status"], "success")

    def test_generate_csv(self):
        result = self.engine.generate_csv(self.data)
        self.assertIsInstance(result, bytes)
        content = result.decode("utf-8")
        self.assertIn("Section,Metric,Value", content)

    def test_generate_html(self):
        result = self.engine.generate_html(self.data)
        self.assertIsInstance(result, bytes)
        content = result.decode("utf-8")
        self.assertIn("<html>", content)
        self.assertIn("RealityLab AI", content)

    def test_generate_pdf(self):
        result = self.engine.generate_pdf(self.data)
        self.assertIsInstance(result, bytes)
        self.assertTrue(result.startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()
