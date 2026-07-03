from typing import Dict
from .models import Profile


class InheritanceEngine:
    """Handles profile inheritance and attribute resolution."""

    def resolve_profile(
        self, profile: Profile, all_profiles: Dict[str, Profile]
    ) -> Profile:
        """Resolves inheritance for a profile by merging attributes from parents."""
        if not profile.parent_id:
            return profile

        visited = set()
        hierarchy = []
        current: Profile | None = profile

        while current:
            if current.id in visited:
                raise ValueError(
                    f"Circular dependency detected for profile {profile.id}"
                )
            visited.add(current.id)
            hierarchy.append(current)

            if current.parent_id:
                if current.parent_id not in all_profiles:
                    raise ValueError(f"Parent profile {current.parent_id} not found")
                current = all_profiles[current.parent_id]
            else:
                current = None

        # Merge attributes from top (root parent) to bottom (child)
        merged_attributes: Dict[str, any] = {}
        for p in reversed(hierarchy):
            merged_attributes.update(p.attributes)

        # Create a new profile with merged attributes
        return Profile(
            id=profile.id,
            name=profile.name,
            attributes=merged_attributes,
            parent_id=profile.parent_id,
        )
