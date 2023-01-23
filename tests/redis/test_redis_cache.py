import os
import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2]
packagePath = os.path.join(str(path), "bot", "libs")
sys.path.append(packagePath)

from cache import CommandKeyBuilder, RedisConnPoolCache, XeltCache
from redis.asyncio.connection import ConnectionPool

DATA = "Hello World!"


@pytest.mark.asyncio
async def test_basic_cache():
    key = CommandKeyBuilder(id=None, command=None)
    connPool = ConnectionPool.from_url("redis://localhost:6379/0")
    cache = XeltCache(connection_pool=connPool)
    await cache.setBasicCache(key=key, value=DATA)
    res = await cache.getBasicCache(key)
    assert (res == DATA) and (isinstance(res, str))  # nosec


@pytest.mark.asyncio
async def test_basic_cache_from_mem():
    memCache = RedisConnPoolCache()
    key = CommandKeyBuilder(id=None, command=None)
    connPool = ConnectionPool.from_url("redis://localhost:6379/0")
    await memCache.addConnPool(key="_", conn_pool_obj=connPool)
    getConnPool = await memCache.getConnPool(key="_")
    if getConnPool is None:
        raise ValueError("Unable to get connection pool from memory cache")
    cache = XeltCache(connection_pool=getConnPool)
    await cache.setBasicCache(key=key, value=DATA)
    assert await cache.getBasicCache(key) == DATA  # nosec
