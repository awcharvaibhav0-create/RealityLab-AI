from typing import Callable, Dict, List
import threading
import logging
from .models import Event

logger = logging.getLogger(__name__)


class EventBus:
    """A thread-safe publish-subscribe event bus."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Event], None]]] = {}
        self._lock = threading.RLock()

    def subscribe(self, topic: str, handler: Callable[[Event], None]) -> None:
        """Subscribe a handler to a specific topic."""
        with self._lock:
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            if handler not in self._subscribers[topic]:
                self._subscribers[topic].append(handler)

    def unsubscribe(self, topic: str, handler: Callable[[Event], None]) -> None:
        """Unsubscribe a handler from a topic."""
        with self._lock:
            if topic in self._subscribers and handler in self._subscribers[topic]:
                self._subscribers[topic].remove(handler)

    def publish(self, event: Event) -> None:
        """Publish an event to all subscribers of the topic and wildcards."""
        with self._lock:
            handlers = self._subscribers.get(event.topic, []).copy()
            handlers.extend(self._subscribers.get("*", []).copy())

        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in event handler for topic {event.topic}: {e}")
