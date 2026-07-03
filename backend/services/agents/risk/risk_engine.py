from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import RiskDetail
from .constants import RiskLevel


class BaseRiskEvaluator(ABC):
    @abstractmethod
    def evaluate(self, scenario: Dict[str, Any]) -> RiskDetail:
        """Evaluate the specific risk and return a RiskDetail."""
        pass

    def _determine_level(self, score: float) -> RiskLevel:
        """Determine risk level based on score (0-100)."""
        if score < 25:
            return RiskLevel.LOW
        if score < 50:
            return RiskLevel.MEDIUM
        if score < 75:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL
