import gc
import logging

logger = logging.getLogger(__name__)

class MemoryManager:
    """Monitors and optimizes memory usage."""
    def optimize(self):
        collected = gc.collect()
        logger.info(f"Memory optimized. Garbage collected {collected} objects.")