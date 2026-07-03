import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from .models import BusinessProfile

logger = logging.getLogger(__name__)


class BusinessProfileEngine:
    """Loads and manages business profiles, handling inheritance and caching."""

    def __init__(self, profiles_dir: str = "knowledge/business_profiles"):
        self.profiles_dir = Path(profiles_dir)
        self._profile_cache: Dict[str, BusinessProfile] = {}
        self._raw_profiles: Dict[str, BusinessProfile] = {}

    def load_all_profiles(self) -> None:
        """Loads all JSON profiles from the profiles directory."""
        if not self.profiles_dir.exists():
            logger.debug(f"Profiles directory {self.profiles_dir} does not exist. Profiles will be skipped.")
            return

        for filepath in self.profiles_dir.glob("*.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    profile = self._parse_profile(data)
                    self._raw_profiles[profile.id] = profile
            except Exception as e:
                logger.error(f"Failed to load profile from {filepath}: {e}")

        # Resolve inheritance and populate cache
        for profile_id, profile in self._raw_profiles.items():
            self._profile_cache[profile_id] = self._resolve_inheritance(profile)

    def get_profile(self, profile_id: str) -> Optional[BusinessProfile]:
        """Retrieves a fully resolved business profile."""
        if not self._profile_cache:
            self.load_all_profiles()

        if profile_id not in self._profile_cache:
            logger.warning(f"Business profile {profile_id} not found.")
            return None

        return self._profile_cache.get(profile_id)

    def get_all_profiles(self) -> Dict[str, BusinessProfile]:
        """Returns all resolved profiles."""
        if not self._profile_cache:
            self.load_all_profiles()
        return self._profile_cache

    def _parse_profile(self, data: Dict[str, Any]) -> BusinessProfile:
        attributes = data.get("attributes", {})
        return BusinessProfile(
            id=data.get("id", ""),
            name=data.get("name", ""),
            business_type=attributes.get("business", {}).get("business_type", ""),
            category=attributes.get("metadata", {}).get("industry", ""),
            parent_id=data.get("parent_id"),
            attributes=attributes,
            financial_defaults=attributes.get("financial", {}),
            operational_rules=attributes.get("operations", {}),
            risk_rules=attributes.get("risk", {}),
            timeline_rules=attributes.get("timeline", {}),
            growth_assumptions=attributes.get("market", {}),
            validation_rules=attributes.get("validation", {}),
            version=attributes.get("metadata", {}).get("version", "1.0.0"),
        )

    def _resolve_inheritance(self, profile: BusinessProfile) -> BusinessProfile:
        """Resolves inheritance using the InheritanceEngine."""
        if not profile.parent_id:
            return profile

        hierarchy = []
        current_id = profile.id
        visited = set()

        while current_id:
            if current_id in visited:
                raise ValueError(
                    f"Circular dependency detected in profile {profile.id}"
                )
            visited.add(current_id)

            curr_profile = self._raw_profiles.get(current_id)
            if not curr_profile:
                raise ValueError(
                    f"Missing parent profile {current_id} for {profile.id}"
                )

            hierarchy.append(curr_profile)
            current_id = curr_profile.parent_id

        # Merge from top parent down to the child
        merged_attrs = {}
        for p in reversed(hierarchy):
            self._deep_merge(merged_attrs, p.attributes)

        # Re-parse the merged profile
        merged_data = {
            "id": profile.id,
            "name": profile.name,
            "parent_id": profile.parent_id,
            "attributes": merged_attrs,
        }
        return self._parse_profile(merged_data)

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """Deeply merges override dictionary into base dictionary."""
        for key, value in override.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
