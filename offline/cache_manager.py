import json
import os
from typing import Optional, Any

class CacheManager:
    """Handles local caching of datasets for offline operations."""
    def __init__(self, cache_dir: str = '.cache'):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def set(self, key: str, data: Any):
        path = os.path.join(self.cache_dir, f"{key}.json")
        with open(path, 'w') as f:
            json.dump(data, f)

    def get(self, key: str) -> Optional[Any]:
        path = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return None