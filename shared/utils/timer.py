import time
from functools import wraps
from typing import Callable, Any, Optional
import logging


class Timer:
    """Context manager for tracking execution time."""

    def __init__(self, name: str = "Timer", logger: Optional[logging.Logger] = None):
        self.name = name
        self.logger = logger
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.log_time()

    def log_time(self) -> None:
        if self.start_time is not None and self.end_time is not None:
            elapsed = self.end_time - self.start_time
            message = f"{self.name} took {elapsed:.4f} seconds"
            if self.logger:
                self.logger.info(message)
            else:
                print(message)

    @property
    def elapsed(self) -> float:
        if self.start_time is None:
            return 0.0
        if self.end_time is None:
            return time.perf_counter() - self.start_time
        return self.end_time - self.start_time


def timer_decorator(
    name: Optional[str] = None, logger: Optional[logging.Logger] = None
) -> Callable:
    """Decorator for tracking execution time of a function."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            timer_name = name or func.__name__
            with Timer(name=timer_name, logger=logger):
                return func(*args, **kwargs)

        return wrapper

    return decorator
