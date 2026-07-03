import logging
from typing import Optional, Dict

from .business_profile_engine import BusinessProfileEngine
from .business_rules_engine import BusinessRulesEngine
from .models import BusinessProfile, ActiveRuleSet

logger = logging.getLogger(__name__)


class LocalKnowledgeBase:
    """
    Facade for the Local Knowledge Base & Business Profile Engine (LKB-BPE).
    Provides unified access to business profiles and business rules.
    """

    def __init__(self, base_dir: str = "knowledge"):
        self.base_dir = base_dir
        self.profile_engine = BusinessProfileEngine(f"{base_dir}/business_profiles")
        self.rules_engine = BusinessRulesEngine(f"{base_dir}/rules")

        self.profile_engine.load_all_profiles()

    def get_business_profile(self, profile_id: str) -> Optional[BusinessProfile]:
        """Retrieves a fully resolved business profile by ID."""
        return self.profile_engine.get_profile(profile_id)

    def get_all_profiles(self) -> Dict[str, BusinessProfile]:
        """Retrieves all loaded business profiles."""
        return self.profile_engine.get_all_profiles()

    def get_active_rules(
        self, business_type: str, scenario_id: Optional[str] = None
    ) -> ActiveRuleSet:
        """Retrieves merged business rules based on priority resolution."""
        return self.rules_engine.load_rules(business_type, scenario_id)

    def reload(self) -> None:
        """Forces a reload of all profiles and rules (useful for cache refreshing)."""
        self.profile_engine = BusinessProfileEngine(
            f"{self.base_dir}/business_profiles"
        )
        self.rules_engine = BusinessRulesEngine(f"{self.base_dir}/rules")
        self.profile_engine.load_all_profiles()
