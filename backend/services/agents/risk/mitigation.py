from dataclasses import dataclass


@dataclass
class MitigationStrategy:
    title: str
    description: str
    impact: str
