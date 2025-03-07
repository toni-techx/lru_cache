import logging
import logging.config

from app.cache import LRUCache
from app.config import LOG_CONFIG, settings

# handler = colorlog.StreamHandler()
# formatter = colorlog.ColoredFormatter(
#     "%(yellow)s%(asctime)s%(reset)s - %(log_color)s%(levelname)s%(reset)s - %(message)s",
#     log_colors={
#         "DEBUG": "cyan",
#         "INFO": "green",
#         "WARNING": "yellow",
#         "ERROR": "red",
#         "CRITICAL": "bold_red",
#     },
# )
# handler.setFormatter(formatter)

# logger = logging.getLogger(__name__)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)


# def initialize_cache():
#     global cache
#     cache = LRUCache(settings.cache_capacity)


def setup_logging():
    logging.config.dictConfig(LOG_CONFIG)
    return logging.getLogger("app")


cache = LRUCache(settings.cache_capacity)
logger = setup_logging()
