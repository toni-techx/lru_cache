import time
from collections import OrderedDict
from threading import Lock
from typing import Optional


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self._cache: OrderedDict = OrderedDict()
        self.lock = Lock()

    def _remove_expired(self, key: str):
        if key in self._cache:
            item = self._cache[key]
            if item["ttl"] and item["ttl"] < time.time():
                del self._cache[key]
                return True
        return False

    def get(self, key: str) -> Optional[str]:
        with self.lock:
            if self._remove_expired(key):
                return None

            if key not in self._cache:
                return None

            self._cache.move_to_end(key)
            return self._cache[key]["value"]

    def set(self, key: str, value: str, ttl: Optional[int] = None):
        with self.lock:
            if self._remove_expired(key):
                # TODO: в задание не указано явно, что делать в случае, если ключ уже существует и просрочен
                pass

            if key in self._cache:
                self._cache[key]["value"] = value
                self._cache[key]["ttl"] = time.time() + ttl if ttl else None
            else:
                if len(self._cache) >= self.capacity:
                    self._cache.popitem(last=False)
                self._cache[key] = {"value": value, "ttl": ttl if ttl else None}

            self._cache.move_to_end(key)

    def delete(self, key: str) -> bool:
        with self.lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def stats(self) -> dict:
        with self.lock:
            return {"size": len(self._cache), "capacity": self.capacity, "items": list(self._cache.keys())}
