from typing import Any, Dict


class ChartGenerator:
    def generate_bar_chart(self, data: Dict[str, float], title: str) -> Any:
        """Mock generating a bar chart"""
        return f"[Bar Chart: {title}]"

    def generate_pie_chart(self, data: Dict[str, float], title: str) -> Any:
        """Mock generating a pie chart"""
        return f"[Pie Chart: {title}]"
