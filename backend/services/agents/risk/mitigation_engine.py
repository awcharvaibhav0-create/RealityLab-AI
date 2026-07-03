from typing import List
from .models import RiskDetail
from .constants import RiskLevel


class MitigationEngine:
    def get_mitigations(self, detail: RiskDetail) -> List[str]:
        mitigations = []
        if detail.level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
            mitigations.append(
                f"Implement immediate monitoring for {detail.category} risk."
            )
            if "budget" in " ".join(detail.factors).lower():
                mitigations.append("Review and reallocate budget immediately.")
            if "market" in detail.category.lower():
                mitigations.append("Diversify market presence to reduce exposure.")
        elif detail.level == RiskLevel.MEDIUM:
            mitigations.append(f"Monitor {detail.category} metrics quarterly.")
        return mitigations
