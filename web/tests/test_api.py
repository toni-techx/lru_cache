from fastapi.testclient import TestClient

from app.cache import LRUCache
from app.models import CacheItem


class TestCache:
    def test_get_cache_stats(self, client: TestClient, setup_cache_with_items: LRUCache):
        response = client.get("/api/v1/cache/stats")
        assert response.status_code == 200
        existing_stats = setup_cache_with_items.stats()
        assert response.json() == existing_stats

    def test_get_cache_item(
        self, client: TestClient, setup_cache_with_items: LRUCache, keys_and_values: dict[str, str]
    ):
        key, value = list(keys_and_values.items())[0]
        response = client.get(f"/api/v1/cache/{key}")
        assert response.status_code == 200
        assert response.json() == {"value": value}

    def test_get_cache_item_not_found(self, client: TestClient, setup_cache_with_items: LRUCache):
        response = client.get("/api/v1/cache/non_existent_key")
        assert response.status_code == 404
        assert response.json() == {"detail": "Key not found or TTL expired"}

    def test_set_cache_item(
        self, client: TestClient, setup_cache_with_items: LRUCache, keys_and_values: dict[str, str]
    ):
        key = list(keys_and_values.keys())[0]
        item = CacheItem(value="new_value", ttl=600)
        response = client.put(f"/api/v1/cache/{key}", json=item.model_dump())

        assert response.status_code == 200
        assert response.json() == {"message": "Item added/updated successfully"}

        response = client.get(f"/api/v1/cache/{key}")
        assert response.status_code == 200
        assert response.json() == {"value": item.value}

        response = client.get("/api/v1/cache/stats")
        assert response.status_code == 200
        assert response.json()["size"] == setup_cache_with_items.stats()["size"]

    def test_set_cache_item_full(self, client: TestClient, setup_cache_with_items: LRUCache):
        item = CacheItem(value="new_value", ttl=60)
        response = client.put("/api/v1/cache/key3", json=item.model_dump())

        assert response.status_code == 200
        assert response.json() == {"message": "Item added/updated successfully"}

        response = client.get("/api/v1/cache/key1")
        assert response.status_code == 404

    def test_delete_cache_item(
        self, client: TestClient, setup_cache_with_items: LRUCache, keys_and_values: dict[str, str]
    ):
        key = list(keys_and_values.keys())[0]
        response = client.delete(f"/api/v1/cache/{key}")
        assert response.status_code == 204

        response = client.get(f"/api/v1/cache/{key}")
        assert response.status_code == 404

    def test_delete_cache_item_not_found(self, client: TestClient, setup_cache_with_items: LRUCache):
        response = client.delete("/api/v1/cache/non_existent_key")
        assert response.status_code == 404
        assert response.json() == {"detail": "Key not found"}
