import logging
import logging.config

from app.cache import LRUCache
from app.config import LOG_CONFIG, settings


def setup_logging():
    logging.config.dictConfig(LOG_CONFIG)
    return logging.getLogger("app")


cache = LRUCache(settings.cache_capacity)
logger = setup_logging()
