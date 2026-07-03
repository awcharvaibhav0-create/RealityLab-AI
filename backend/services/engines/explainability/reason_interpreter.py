from typing import List
from .decision_trace import DecisionTrace

class ReasonInterpreter:
    """Translates a technical decision trace into human-readable text."""
    def interpret(self, trace: DecisionTrace) -> str:
        lines = ["Decision Rationale:"]
        for step in trace.get_trace():
            lines.append(f"- {step.action} (Context: {step.context})")
        return '\n'.join(lines)