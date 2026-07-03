import logging
from typing import Any, Dict
from backend.services.core.base_agent import BaseAgent
from backend.services.core.types import Context, ReturnType

from .config import RiskConfig
from .validator import RiskValidator
from .models import RiskResult, RiskDetail
from .constants import RiskLevel

from .financial_risk import FinancialRiskEvaluator
from .market_risk import MarketRiskEvaluator
from .operational_risk import OperationalRiskEvaluator
from .customer_risk import CustomerRiskEvaluator
from .execution_risk import ExecutionRiskEvaluator
from .competition_risk import CompetitionRiskEvaluator
from .seasonal_risk import SeasonalRiskEvaluator
from .supply_chain_risk import SupplyChainRiskEvaluator
from .regulatory_risk import RegulatoryRiskEvaluator
from .business_continuity import BusinessContinuityRiskEvaluator

from .mitigation_engine import MitigationEngine
from .confidence_engine import ConfidenceEngine

logger = logging.getLogger(__name__)

from shared.knowledge.local_knowledge_base import LocalKnowledgeBase


class RiskAgent(BaseAgent):
    def __init__(self, name: str = "RiskAgent", lkb: LocalKnowledgeBase = None):
        super().__init__(name)
        self.evaluators = []
        self.config = RiskConfig()
        self.mitigation_engine = MitigationEngine()
        self.confidence_engine = ConfidenceEngine()
        self.validator = RiskValidator()
        self.lkb = lkb or LocalKnowledgeBase()

    def _do_initialize(self, config: Context) -> None:
        self.config = RiskConfig(weights=config.get("weights"))
        self.evaluators = [
            FinancialRiskEvaluator(),
            MarketRiskEvaluator(),
            OperationalRiskEvaluator(),
            CustomerRiskEvaluator(),
            ExecutionRiskEvaluator(),
            CompetitionRiskEvaluator(),
            SeasonalRiskEvaluator(),
            SupplyChainRiskEvaluator(),
            RegulatoryRiskEvaluator(),
            BusinessContinuityRiskEvaluator(),
        ]
        logger.info(f"{self.name} initialized with {len(self.evaluators)} evaluators.")

    def validate(self, task: Any) -> bool:
        super().validate(task)
        self.validator.validate(task)
        return True

    def _determine_overall_level(self, score: float) -> RiskLevel:
        if score < 25:
            return RiskLevel.LOW
        if score < 50:
            return RiskLevel.MEDIUM
        if score < 75:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL

    def _do_execute(self, task: Any, context: Context) -> ReturnType:
        scenario_name = task.get("name", "Unknown Scenario")
        logger.info(f"Executing risk assessment for scenario: {scenario_name}")

        details: Dict[str, RiskDetail] = {}
        overall_score = 0.0

        for evaluator in self.evaluators:
            detail = evaluator.evaluate(task)
            # evaluator must now return a RiskDetail with level and reason
            details[detail.category] = detail

            weight = self.config.weights.get(detail.category, 0.1)
            overall_score += detail.score * weight

        confidence = "High" if task.get("historical_data") else "Medium"
        overall_level = self._determine_overall_level(overall_score).name.title()

        result = RiskResult(
            scenario=scenario_name,
            financial_risk=details.get(
                "financial", RiskDetail("financial", "Low", 0.0, "")
            ).level,
            market_risk=details.get(
                "market", RiskDetail("market", "Low", 0.0, "")
            ).level,
            competition_risk=details.get(
                "competition", RiskDetail("competition", "Low", 0.0, "")
            ).level,
            customer_risk=details.get(
                "customer", RiskDetail("customer", "Low", 0.0, "")
            ).level,
            operational_risk=details.get(
                "operational", RiskDetail("operational", "Low", 0.0, "")
            ).level,
            overall_score=round(overall_score),
            overall_level=overall_level,
            confidence=confidence,
            details=details,
        )

        return {"status": "success", "data": result}

    def _do_cleanup(self) -> None:
        self.evaluators = []
        logger.info(f"{self.name} cleaned up.")
