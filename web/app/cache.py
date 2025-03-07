import time
from collections import OrderedDict
from threading import Lock
from typing import Any, Optional


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: OrderedDict = OrderedDict()
        self.lock = Lock()

    def _remove_expired(self, key: str):
        if key in self.cache:
            item = self.cache[key]
            if item["ttl"] and item["ttl"] < time.time():
                del self.cache[key]
                return True
        return False

    def get(self, key: str) -> Optional[str]:
        with self.lock:
            if self._remove_expired(key):
                return None

            if key not in self.cache:
                return None

            self.cache.move_to_end(key)
            return self.cache[key]["value"]

    def set(self, key: str, value: str, ttl: Optional[int] = None):
        with self.lock:
            if self._remove_expired(key):
                # TODO: в задание не указано явно, что делать в случае, если ключ уже существует и просрочен
                pass

            if key in self.cache:
                self.cache[key]["value"] = value
                self.cache[key]["ttl"] = time.time() + ttl if ttl else None
            else:
                if len(self.cache) >= self.capacity:
                    self.cache.popitem(last=False)
                self.cache[key] = {"value": value, "ttl": ttl if ttl else None}

            self.cache.move_to_end(key)

    def delete(self, key: str) -> bool:
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False

    def stats(self) -> dict:
        with self.lock:
            return {"size": len(self.cache), "capacity": self.capacity, "items": list(self.cache.keys())}
