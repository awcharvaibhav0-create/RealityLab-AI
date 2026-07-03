import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import json

from .models import RuleSet, ActiveRuleSet, RulePriority

logger = logging.getLogger(__name__)


class BusinessRulesEngine:
    """Manages all configurable business logic, handling inheritance and priority resolution."""

    def __init__(self, rules_dir: str = "knowledge/rules"):
        self.rules_dir = Path(rules_dir)
        self._rules_cache: Dict[str, List[RuleSet]] = {}

    def load_rules(
        self, business_type: str, scenario_id: Optional[str] = None
    ) -> ActiveRuleSet:
        """Loads and merges rules according to priority for a specific business type and scenario."""
        if not self._rules_cache:
            self._load_all_rules()

        active_rules: Dict[str, Any] = {}

        # 1. Global Defaults (Priority 5)
        self._apply_rules(
            active_rules, self._get_rules_by_priority(RulePriority.GLOBAL_DEFAULT)
        )

        # 2. Industry Defaults (Priority 4)
        self._apply_rules(
            active_rules,
            self._get_rules_by_priority(
                RulePriority.INDUSTRY_DEFAULT, target_id=business_type
            ),
        )

        # 3. Scenario Modifier (Priority 3)
        if scenario_id:
            self._apply_rules(
                active_rules,
                self._get_rules_by_priority(
                    RulePriority.SCENARIO_MODIFIER, target_id=scenario_id
                ),
            )

        # 4. Business Profile (Priority 2)
        self._apply_rules(
            active_rules,
            self._get_rules_by_priority(
                RulePriority.BUSINESS_PROFILE, target_id=business_type
            ),
        )

        # 5. User Override (Priority 1) - Applied dynamically during simulation

        return ActiveRuleSet(business_type=business_type, active_rules=active_rules)

    def _load_all_rules(self) -> None:
        """Loads all JSON rules from the rules directories."""
        if not self.rules_dir.exists():
            logger.warning(f"Rules directory {self.rules_dir} does not exist.")
            return

        for category_dir in self.rules_dir.iterdir():
            if category_dir.is_dir():
                for filepath in category_dir.glob("*.json"):
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            priority_str = data.get("priority", "GLOBAL_DEFAULT")
                            priority = getattr(
                                RulePriority,
                                priority_str.upper(),
                                RulePriority.GLOBAL_DEFAULT,
                            )

                            rule_set = RuleSet(
                                id=data.get("id", filepath.stem),
                                category=category_dir.name,
                                rules=data.get("rules", {}),
                                priority=priority,
                                version=data.get("version", "1.0.0"),
                            )
                            if category_dir.name not in self._rules_cache:
                                self._rules_cache[category_dir.name] = []
                            self._rules_cache[category_dir.name].append(rule_set)
                    except Exception as e:
                        logger.error(f"Failed to load rule from {filepath}: {e}")

    def _get_rules_by_priority(
        self, priority: RulePriority, target_id: Optional[str] = None
    ) -> List[RuleSet]:
        matching = []
        for cat, rule_sets in self._rules_cache.items():
            for rs in rule_sets:
                if rs.priority == priority:
                    if target_id and rs.id != target_id:
                        continue
                    matching.append(rs)
        return matching

    def _apply_rules(
        self, active_rules: Dict[str, Any], rule_sets: List[RuleSet]
    ) -> None:
        """Merges rules into active_rules. Higher priority rules overwrite lower ones. Logs conflicts."""
        for rs in rule_sets:
            self._deep_merge(active_rules, rs.rules, rs.id)

    def _deep_merge(
        self, base: Dict[str, Any], new: Dict[str, Any], source_id: str
    ) -> None:
        for key, value in new.items():
            if key in base:
                if isinstance(base[key], dict) and isinstance(value, dict):
                    self._deep_merge(base[key], value, source_id)
                else:
                    if base[key] != value:
                        logger.info(
                            f"Conflict detected for rule '{key}': replacing {base[key]} with {value} from '{source_id}'"
                        )
                    base[key] = value
            else:
                base[key] = value
