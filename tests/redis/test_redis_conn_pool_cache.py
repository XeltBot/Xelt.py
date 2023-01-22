import os
import sys
from pathlib import Path

import pytest
import redis.asyncio as redis
from dotenv import load_dotenv
from redis.asyncio.connection import ConnectionPool

path = Path(__file__).parents[2]
packagePath = os.path.join(str(path), "bot", "libs")
envPath = os.path.join(str(path), "bot", ".env")
sys.path.append(packagePath)

from cache import RedisConnPoolCache

load_dotenv(dotenv_path=envPath)


@pytest.mark.asyncio
async def test_pool_mem_cache_add():
    connPool = ConnectionPool(max_connections=25)
    memCache = RedisConnPoolCache()
    await memCache.addConnPool(key="conn1", conn_pool_obj=connPool)
    assert isinstance(await memCache.getConnPool(key="conn1"), ConnectionPool)  # nosec


@pytest.mark.asyncio
async def test_pool_mem_cache_delete():
    connPool = ConnectionPool(max_connections=25)
    memCache = RedisConnPoolCache()
    await memCache.addConnPool(key="conn1", conn_pool_obj=connPool)
    assert await memCache.deleteConnPool(key="conn1") is True  # nosec


@pytest.mark.asyncio
async def test_pool_mem_cache_set():
    connPool = ConnectionPool(max_connections=25)
    memCache = RedisConnPoolCache()
    await memCache.setConnPool(key="conn1", conn_pool_obj=connPool)
    await memCache.setConnPool(key="conn2", conn_pool_obj=connPool)
    assert (  # nosec
        await memCache.deleteConnPool(key="conn1") is True
        and await memCache.deleteConnPool(key="conn2") is True
    )


@pytest.mark.asyncio
async def test_pool_mem_cache_clear():
    memCache = RedisConnPoolCache()
    for i, _ in enumerate(range(5)):
        connPool = ConnectionPool(max_connections=25)
        await memCache.addConnPool(key=f"conn{i}", conn_pool_obj=connPool)

    await memCache.clearConnPool()
    assert len(await memCache.getAllConnPool()) == 0  # nosec


@pytest.mark.asyncio
async def test_pool_mem_integration():
    connPool = ConnectionPool(max_connections=25)
    memCache = RedisConnPoolCache()
    await memCache.addConnPool(key="conn1", conn_pool_obj=connPool)
    currPool = await memCache.getConnPool(key="conn1")
    r = redis.Redis(connection_pool=currPool, decode_responses=True)
    await r.set("foo", "bar")
    res = await r.get("foo")
    await r.close(close_connection_pool=True)
    assert res == b"bar"  # nosec
