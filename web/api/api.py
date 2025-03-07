from fastapi import APIRouter, HTTPException, Response, status

from app.core import cache
from app.middleware import logger
from app.models import CacheItem

router = APIRouter(prefix="/api/v1")


@router.get("/cache/stats")
async def get_stats():
    stats = cache.stats()
    logger.info("Cache stats requested: %s", stats)
    return stats


@router.get("/cache/{key}")
async def get_cache(key: str):
    value = cache.get(key)
    if value is None:
        logger.warning("Cache miss for key: %s", key)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found or TTL expired")

    logger.info("Cache hit for key: %s", key)
    return {"value": value}


@router.put("/cache/{key}")
async def set_cache(key: str, item: CacheItem):
    cache.set(key, item.value, item.ttl)
    logger.info("Cache set: key=%s, ttl=%s", key, item.ttl)
    return {"message": "Item added/updated successfully"}


@router.delete("/cache/{key}")
async def delete_cache(key: str):
    if not cache.delete(key):
        logger.warning("Attempted to delete non-existent key: %s", key)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")

    logger.info("Cache deleted: key=%s", key)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
