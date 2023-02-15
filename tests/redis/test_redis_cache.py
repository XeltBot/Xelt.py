import json
import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2]
sys.path.append(str(path))

from redis.asyncio.connection import ConnectionPool

from bot.libs.cache import CommandKeyBuilder, MemStorage, XeltCache

DATA = "Hello World!"


@pytest.fixture(autouse=True, scope="session")
def load_conn_pool():
    return ConnectionPool.from_url("redis://localhost:6379/0")


@pytest.fixture(autouse=True, scope="session")
def load_json_data():
    fileDir = Path(__file__).parent.joinpath("data")
    with open(fileDir.joinpath("redis_test.json"), "r") as f:
        data = json.load(f)
        return data


@pytest.mark.asyncio
async def test_basic_cache(load_conn_pool):
    key = CommandKeyBuilder(id=None, command=None)
    cache = XeltCache(connection_pool=load_conn_pool)
    await cache.setBasicCache(key=key, value=DATA)
    res = await cache.getBasicCache(key)
    assert (res == DATA) and (isinstance(res, str))  # nosec


@pytest.mark.asyncio
async def test_basic_cache_from_mem():
    key = CommandKeyBuilder(id=None, command=None)
    memStore = MemStorage()
    memStore.set("redis_conn_pool", ConnectionPool.from_url("redis://localhost:6379/0"))
    getConnPool = memStore.get("redis_conn_pool")
    if getConnPool is None:
        raise ValueError("Unable to get conn pool from mem cache")
    cache = XeltCache(connection_pool=getConnPool)
    await cache.setBasicCache(key=key, value=DATA)
    res = await cache.getBasicCache(key=key)
    assert (res == DATA) and (isinstance(res, str))  # nosec


@pytest.mark.asyncio
async def test_json_cache(load_json_data):
    connPool = ConnectionPool().from_url("redis://localhost:6379/0")
    cache = XeltCache(connection_pool=connPool)
    await cache.setJSONCache(key="main3", value=load_json_data, ttl=5)
    res = await cache.getJSONCache(key="main3")
    assert (res == load_json_data) and (isinstance(res, dict))  # nosec


@pytest.mark.asyncio
async def test_json_cache_from_mem(load_json_data):
    memStore = MemStorage()
    memStore.set(
        "redis_conn_pool2", ConnectionPool.from_url("redis://localhost:6379/0")
    )
    getConnPool = memStore.get("redis_conn_pool2")
    if getConnPool is None:
        raise ValueError("Unable to get conn pool from mem cache")
    cache = XeltCache(connection_pool=getConnPool)
    await cache.setJSONCache(key="main4", value=load_json_data, ttl=5)
    res = await cache.getJSONCache(key="main4")
    assert (res == load_json_data) and (isinstance(res, dict))  # nosec
