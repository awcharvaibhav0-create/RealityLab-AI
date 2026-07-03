from typing import Any, Dict


class ObservabilityManager:
    def initialize(self) -> None:
        pass

    def start(self) -> None:
        pass

    def collect(self) -> Dict[str, Any]:
        return {"metrics": {}}

    def health_check(self) -> Dict[str, str]:
        return {"status": "healthy"}
