import json
import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2].joinpath("bot")
sys.path.append(str(path))

from libs.cache import CommandKeyBuilder, XeltCache
from redis.asyncio.connection import ConnectionPool


@pytest.fixture(autouse=True, scope="session")
def load_str_data():
    return "Hello World!"


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
async def test_basic_cache(load_conn_pool, load_str_data):
    key = CommandKeyBuilder(id=None, command=None)
    cache = XeltCache(connection_pool=load_conn_pool)
    await cache.setBasicCache(key=key, value=load_str_data)
    res = await cache.getBasicCache(key)
    assert (res == load_str_data.encode()) and (isinstance(res, bytes))  # nosec


@pytest.mark.asyncio
async def test_json_cache(load_json_data):
    connPool = ConnectionPool().from_url("redis://localhost:6379/0")
    cache = XeltCache(connection_pool=connPool)
    await cache.setJSONCache(key="main3", value=load_json_data, ttl=5)
    res = await cache.getJSONCache(key="main3")
    assert (res == load_json_data) and (isinstance(res, dict))  # nosec


@pytest.mark.asyncio
async def test_cache_exists(load_str_data):
    connPool = ConnectionPool().from_url("redis://localhost:6379/0")
    cache = XeltCache(connection_pool=connPool)
    await cache.setBasicCache(key="main5", value=load_str_data, ttl=15)
    res = await cache.cacheExists(key="main5")
    assert res is True  # nosec
