from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List


class RulePriority(Enum):
    GLOBAL_DEFAULT = 1
    INDUSTRY_DEFAULT = 2
    SCENARIO_MODIFIER = 3
    BUSINESS_PROFILE = 4
    BUSINESS_RULES = 5
    SCENARIO_OVERRIDE = 6


@dataclass
class RuleSet:
    id: str = ""
    name: str = ""
    category: str = ""
    version: str = ""
    priority: RulePriority = RulePriority.BUSINESS_RULES
    target_id: str = ""
    rules: Dict[str, Any] = field(default_factory=dict)


class ActiveRuleSet:
    def __init__(self, business_type="", active_rules=None):
        self.business_type = business_type
        self.active_rules = active_rules or {}


class KnowledgeModels:
    pass


@dataclass
class BusinessProfile:
    id: str = ""
    name: str = ""
    type: str = ""
    business_type: str = ""
    category: str = ""
    base_metrics: Dict[str, Any] = field(default_factory=dict)
    attributes: Dict[str, Any] = field(default_factory=dict)
    financial_defaults: Dict[str, Any] = field(default_factory=dict)
    operational_rules: Dict[str, Any] = field(default_factory=dict)
    risk_rules: Dict[str, Any] = field(default_factory=dict)
    timeline_rules: Dict[str, Any] = field(default_factory=dict)
    market_rules: Dict[str, Any] = field(default_factory=dict)
    growth_assumptions: Dict[str, Any] = field(default_factory=dict)
    validation_rules: Dict[str, Any] = field(default_factory=dict)
    version: str = "1.0.0"
    rules: List[Any] = field(default_factory=list)
    parent: str = None
    parent_id: str = None


# Backward-compatible alias used by inheritance helpers.
Profile = BusinessProfile
