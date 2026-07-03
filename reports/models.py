from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum


class ReportFormat(Enum):
    PDF = "pdf"
    HTML = "html"
    MARKDOWN = "md"
    JSON = "json"
    CSV = "csv"


@dataclass
class ReportSection:
    title: str
    content: str
    order: int = 0
    charts: List[Any] = field(default_factory=list)


@dataclass
class ReportData:
    title: str
    author: str
    sections: List[ReportSection] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
