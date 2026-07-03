from typing import Dict, Optional
from .constants import RiskCategory


class RiskConfig:
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or {
            RiskCategory.FINANCIAL.value: 0.2,
            RiskCategory.MARKET.value: 0.15,
            RiskCategory.OPERATIONAL.value: 0.15,
            RiskCategory.CUSTOMER.value: 0.1,
            RiskCategory.EXECUTION.value: 0.1,
            RiskCategory.COMPETITION.value: 0.1,
            RiskCategory.SEASONAL.value: 0.05,
            RiskCategory.SUPPLY_CHAIN.value: 0.05,
            RiskCategory.REGULATORY.value: 0.05,
            RiskCategory.BUSINESS_CONTINUITY.value: 0.05,
        }
