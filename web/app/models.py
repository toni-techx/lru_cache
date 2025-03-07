from typing import Optional

from pydantic import BaseModel, Field


class CacheItem(BaseModel):
    value: str
    ttl: Optional[int] = Field(None, gt=0)


class CacheStats(BaseModel):
    size: int
    capacity: int
    items: list[str]
