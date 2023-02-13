import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv
from redis.asyncio.connection import ConnectionPool

path = Path(__file__).parents[2]
packagePath = os.path.join(str(path), "bot", "libs")
envPath = os.path.join(str(path), "bot", ".env")
sys.path.append(packagePath)

from cache import MemStorage

load_dotenv(dotenv_path=envPath)


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
    doesKeyExists = memStore.get(key="main2")
    assert doesKeyExists is True  # nosec


def test_mem_storage_delete(load_conn_pool):
    memStore = MemStorage()
    memStore.add(key="main3", value=load_conn_pool)
    memStore.delete(key="main3")
    doesKeyExists = memStore.get(key="main3")
    assert doesKeyExists is False  # nosec
