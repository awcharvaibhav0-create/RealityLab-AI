import json
from typing import Dict, Any


class ResponseParser:
    def parse(self, raw_response: str) -> Dict[str, Any]:
        """Parses the raw string response from the LLM into a dictionary."""
        try:
            # Simple cleanup for markdown json blocks if present
            cleaned = raw_response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse response as JSON: {e}")
