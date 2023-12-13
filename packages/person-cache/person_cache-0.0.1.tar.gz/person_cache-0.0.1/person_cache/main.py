import time
import json
from datetime import date
from decimal import *
from functools import wraps

from redis import asyncio as aioredis


class RedisSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        redis_url_full = kwargs.get("url_redis")
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.redis = aioredis.from_url(
                redis_url_full, encoding="utf-8", decode_responses=True
            )
        return cls._instance
    
    @classmethod
    def cache_response(cls, key_prefix, expire_time, skip_args = 0):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                if skip_args > 0:
                    args_list = list(args)
                    args_list = args_list[skip_args:]
                    args_new = tuple(args_list)
                    key=f"{key_prefix}:{args_new}:{kwargs}"
                else:
                    key=f"{key_prefix}:{args}:{kwargs}"
                                    
                cached = await cls().redis.get(key)

                if cached:
                    data = cached
                else:
                    data_dict = await func(*args, **kwargs)
                    data = json.dumps(data_dict, cls=CustomEncoder)
                    await cls().redis.setex(key, expire_time, data
                    )

                return json.loads(data)
            return wrapper
        return decorator
    

class LocalCache:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.cache = {}
        return cls._instance
    

    def get_data(self, key):
        if key in self.cache:
            data, expiration_time = self.cache[key]
            if time.time() < expiration_time:
                return data
            else:
                del self.cache[key]
        return None

    def set_data(self, key, value, ttl_seconds=60):
        expiration_time = time.time() + ttl_seconds
        self.cache[key] = (value, expiration_time)
    
    @classmethod
    def cache_response(cls, key_prefix, expire_time, skip_args = 0):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                if skip_args > 0:
                    args_list = list(args)
                    args_list = args_list[skip_args:]
                    args_new = tuple(args_list)
                    key=f"{key_prefix}:{args_new}:{kwargs}"
                else:
                    key=f"{key_prefix}:{args}:{kwargs}"
                
                cached = cls().get_data(key=key)

                if cached:
                    data = cached
                else:
                    data_dict = await func(*args, **kwargs)
                    data = json.dumps(data_dict, cls=CustomEncoder)
                    cls().set_data(key=f"{key_prefix}:{args}:{kwargs}", value=data, ttl_seconds=expire_time)

                return json.loads(data)
            return wrapper
        return decorator


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return str(obj)
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return super().default(obj)