import logging
from typing import Dict, Any

from .models import DecisionContext, TokenUsage
from .prompt_builder import PromptBuilder
from .api_client import APIClient
from .response_parser import ResponseParser
from .response_validator import ResponseValidator
from .formatter import Formatter
from .fallback_engine import FallbackEngine
from .cache import Cache
from .rate_limiter import RateLimiter
from .cost_tracker import CostTracker

logger = logging.getLogger(__name__)


class DecisionAgent:
    def __init__(self):
        self.prompt_builder = PromptBuilder()
        self.api_client = APIClient()
        self.parser = ResponseParser()
        self.validator = ResponseValidator()
        self.formatter = Formatter()
        self.fallback_engine = FallbackEngine()
        self.cache = Cache()
        self.rate_limiter = RateLimiter(calls_per_second=2.0)
        self.cost_tracker = CostTracker()

    def generate_recommendation(self, context_data: Dict[str, Any]) -> str:
        """Main entry point to convert analysis into an executive recommendation."""
        try:
            context = DecisionContext(analysis_data=context_data)
            prompt = self.prompt_builder.build_prompt(context)

            # Check cache
            cached_response = self.cache.get(prompt)
            if cached_response:
                logger.info("Cache hit for prompt.")
                raw_response = cached_response
            else:
                logger.info("Cache miss, calling API.")
                self.rate_limiter.wait()
                raw_response, usage_data = self.api_client.generate_content(prompt)
                self.cache.set(prompt, raw_response)

                # Track costs
                usage = TokenUsage(**usage_data)
                self.cost_tracker.add_usage(usage)

            parsed = self.parser.parse(raw_response)
            decision = self.validator.validate(parsed)
            return self.formatter.format_recommendation(decision)

        except Exception as e:
            logger.error(f"Error generating recommendation: {e}")
            fallback = self.fallback_engine.get_fallback_decision(str(e))
            return self.formatter.format_recommendation(fallback)
