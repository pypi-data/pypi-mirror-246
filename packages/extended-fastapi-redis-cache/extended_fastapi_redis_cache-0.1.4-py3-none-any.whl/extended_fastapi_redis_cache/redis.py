"""redis.py"""
import os
from typing import Tuple

import redis.asyncio as redis

from extended_fastapi_redis_cache.enums import RedisStatus


async def redis_connect(host_url: str) -> Tuple[RedisStatus, redis.client.Redis]:
    """Attempt to connect to `host_url` and return a Redis client instance if successful."""
    return await _connect(host_url)


async def _connect(host_url: str) -> Tuple[RedisStatus, redis.client.Redis]:  # pragma: no cover
    try:
        redis_client = redis.Redis(host_url)
        if await redis_client.ping():
            return (RedisStatus.CONNECTED, redis_client)
        return (RedisStatus.CONN_ERROR, None)
    except redis.AuthenticationError:
        return (RedisStatus.AUTH_ERROR, None)
    except redis.ConnectionError:
        return (RedisStatus.CONN_ERROR, None)


def _connect_fake() -> Tuple[RedisStatus, redis.client.Redis]:
    return
    # from fakeredis import FakeRedis
    # return (RedisStatus.CONNECTED, FakeRedis())
