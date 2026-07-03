from typing import Any, Dict
import threading


class SharedContext:
    """Thread-safe key-value store for sharing data across tasks."""

    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._lock = threading.RLock()

    def set(self, key: str, value: Any) -> None:
        """Set a value in the context."""
        with self._lock:
            self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the context, or default if not found."""
        with self._lock:
            return self._data.get(key, default)

    def remove(self, key: str) -> None:
        """Remove a key from the context."""
        with self._lock:
            if key in self._data:
                del self._data[key]

    def clear(self) -> None:
        """Clear all data from the context."""
        with self._lock:
            self._data.clear()

    def get_all(self) -> Dict[str, Any]:
        """Return a copy of all data in the context."""
        with self._lock:
            return dict(self._data)
