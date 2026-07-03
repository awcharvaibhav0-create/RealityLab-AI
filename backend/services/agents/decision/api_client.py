import os
from google import genai
from typing import Tuple


class APIClient:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY", "dummy_key")
        self.client = genai.Client(api_key=api_key)

    def generate_content(self, prompt: str) -> Tuple[str, dict]:
        """Calls Gemini API and returns response text and token usage metadata."""
        # Note: in real use, you'd specify gemini-2.5-flash as the model.
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        usage = {
            "prompt_tokens": (
                getattr(response.usage_metadata, "prompt_token_count", 0)
                if hasattr(response, "usage_metadata")
                else 0
            ),
            "completion_tokens": (
                getattr(response.usage_metadata, "candidates_token_count", 0)
                if hasattr(response, "usage_metadata")
                else 0
            ),
            "total_tokens": (
                getattr(response.usage_metadata, "total_token_count", 0)
                if hasattr(response, "usage_metadata")
                else 0
            ),
        }
        return response.text, usage
