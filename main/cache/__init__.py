import urllib
from abc import ABCMeta

from flask import request
from flask_caching import Cache
from flask_jwt_extended import get_jwt_identity
from flask_restx import Resource
from redis import StrictRedis

from config import config_by_name

cache = Cache()


redis_config = config_by_name["cache"]
redis_client = StrictRedis(
    redis_config["CACHE_REDIS_HOST"], redis_config["CACHE_REDIS_PORT"], charset="utf-8", decode_responses=True
)


def cache_key() -> str:
    """
    This function is used to create a cache key according to path, logged-in user, and request params.
    :return: str
    """
    args = request.args
    path = request.path + "?"
    if "Authorization" in request.headers:
        path += f"user_role={get_jwt_identity()['role']}&"
    key = path + urllib.parse.urlencode([(k, v) for k in sorted(args) for v in sorted(args.getlist(k))])
    return key


def clear_cache():
    """
    This function is used to remove all caching keys of a particular path.
    :return:
    """
    key_pattern = "flask_cache_" + request.path + "*"
    for key in redis_client.scan_iter(match=key_pattern):
        redis_client.delete(key)


def cache_decorator(func):
    def wrapper(self, *args, **kwargs):
        return cache.cached(key_prefix=cache_key, timeout=60)(func)(self, *args, **kwargs)

    return wrapper


def clear_cache_decorator(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        clear_cache()
        return result

    return wrapper


class CacheResourceMeta(ABCMeta):
    def __new__(mcls, name, bases, attrs):
        if "get" in attrs:
            attrs["get"] = cache_decorator(attrs["get"])
        if "post" in attrs:
            attrs["post"] = clear_cache_decorator(attrs["post"])
        if "put" in attrs:
            attrs["put"] = clear_cache_decorator(attrs["put"])
        if "delete" in attrs:
            attrs["delete"] = clear_cache_decorator(attrs["delete"])
        return super().__new__(mcls, name, bases, attrs)


class CacheResource(Resource, metaclass=CacheResourceMeta):
    pass
