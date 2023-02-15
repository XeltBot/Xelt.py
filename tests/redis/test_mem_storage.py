import sys
from pathlib import Path

import pytest
import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool

path = Path(__file__).parents[2]
sys.path.append(str(path))

from bot.libs.cache import MemStorage


@pytest.fixture(autouse=True, scope="session")
def load_conn_pool():
    return ConnectionPool(max_connections=25)


def test_mem_storage_add(load_conn_pool):
    memStore = MemStorage()
    memStore.add(key="conn1", value=load_conn_pool)
    assert isinstance(memStore.get(key="conn1"), ConnectionPool)  # nosec


def test_mem_storage_get(load_conn_pool):
    memStore = MemStorage()
    memStore.set(key="main", value=load_conn_pool)
    res = memStore.get(key="main")
    assert isinstance(res, ConnectionPool)  # nosec


def test_mem_storage_exists(load_conn_pool):
    memStore = MemStorage()
    memStore.add(key="main2", value=load_conn_pool)
    doesKeyExists = memStore.exists(key="main2")
    assert doesKeyExists is True  # nosec


def test_mem_storage_delete(load_conn_pool):
    memStore = MemStorage()
    memStore.add(key="main3", value=load_conn_pool)
    memStore.delete(key="main3")
    doesKeyExists = memStore.exists(key="main3")
    assert doesKeyExists is False  # nosec


def test_mem_storage_clear(load_conn_pool):
    memStore = MemStorage()
    for i in enumerate(range(10)):
        memStore.add(key=f"main{i}", value=load_conn_pool)
    memStore.clear()
    currAmount = len(memStore.getAll())
    assert currAmount == 0  # nosec


@pytest.mark.asyncio
async def test_mem_storage_integration(load_conn_pool):
    memStore = MemStorage()
    memStore.add(key="main", value=load_conn_pool)
    currConnPool = memStore.get(key="main")
    r = redis.Redis(connection_pool=currConnPool, decode_responses=True)
    await r.set("foo", "bar")
    res = await r.get("foo")
    await r.close(close_connection_pool=True)
    assert res == b"bar"  # nosec
