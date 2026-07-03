import hashlib
from typing import Optional, Dict


class Cache:
    def __init__(self):
        self._storage: Dict[str, str] = {}

    def _generate_key(self, prompt: str) -> str:
        return hashlib.md5(prompt.encode("utf-8")).hexdigest()

    def get(self, prompt: str) -> Optional[str]:
        return self._storage.get(self._generate_key(prompt))

    def set(self, prompt: str, response: str) -> None:
        self._storage[self._generate_key(prompt)] = response
