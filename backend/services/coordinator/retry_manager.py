import time
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)


class RetryManager:
    """Handles execution of functions with exponential backoff retry logic."""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def execute_with_retry(self, action: Callable[[], Any], task_id: str) -> Any:
        """Executes the action and retries on failure with exponential backoff."""
        retries = 0
        while True:
            try:
                return action()
            except Exception as e:
                retries += 1
                if retries > self.max_retries:
                    logger.error(
                        f"Task {task_id} failed after {self.max_retries} retries: {e}"
                    )
                    raise e

                delay = self.base_delay * (2 ** (retries - 1))
                logger.warning(
                    f"Task {task_id} failed (attempt {retries}/{self.max_retries}). Retrying in {delay}s... Error: {e}"
                )
                time.sleep(delay)
