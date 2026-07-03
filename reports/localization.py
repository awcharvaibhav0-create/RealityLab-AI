class LocalizationManager:
    def __init__(self, language: str = "en"):
        self.language = language
        self._strings = {
            "en": {
                "report_title": "Report",
                "executive_summary": "Executive Summary",
            },
            "es": {
                "report_title": "Reporte",
                "executive_summary": "Resumen Ejecutivo",
            },
        }

    def get_string(self, key: str) -> str:
        return self._strings.get(self.language, {}).get(key, key)
