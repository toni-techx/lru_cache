from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient

from api.api import cache
from app.cache import LRUCache
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def keys_and_values():
    return {
        "key1": "value1",
        "key2": "value2",
    }


@pytest.fixture
def setup_cache_with_items(keys_and_values: Dict[str, str]) -> LRUCache:
    for key, value in keys_and_values.items():
        cache.set(key, value)
    return cache


@pytest.fixture
def setup_cache_with_items_and_ttl(keys_and_values: Dict[str, str], ttl: int = 1) -> LRUCache:
    for key, value in keys_and_values.items():
        cache.set(key, value, ttl)
    return cache
