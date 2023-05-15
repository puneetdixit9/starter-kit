from flask_caching import Cache
from redis import StrictRedis

from config import config_by_name

cache = Cache()


redis_config = config_by_name["cache"]
redis_client = StrictRedis(
    redis_config["CACHE_REDIS_HOST"], redis_config["CACHE_REDIS_PORT"], charset="utf-8", decode_responses=True
)
