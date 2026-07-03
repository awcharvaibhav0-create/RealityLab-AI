import json
from .models import DecisionContext


class ContextBuilder:
    def build(self, context: DecisionContext) -> str:
        """Builds a string representation of the context for the prompt."""
        return json.dumps(context.analysis_data, indent=2)
