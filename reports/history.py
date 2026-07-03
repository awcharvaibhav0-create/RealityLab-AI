from datetime import datetime


class ReportHistory:
    def __init__(self, log_file: str = "report_history.json"):
        self.log_file = log_file

    def log_report_generation(self, report_id: str, format: str):
        record = {
            "report_id": report_id,
            "format": format,
            "timestamp": datetime.now().isoformat(),
        }
        # In a real app, read, append, write. Here we just print for placeholder.
        print(f"Logged report generation: {record}")
