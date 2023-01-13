import asyncio
import os
import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2]
packagePath = os.path.join(str(path), "bot", "libs")
sys.path.append(packagePath)

from cache import CommandKeyBuilder, XeltCache
from utils import RedisClient


@pytest.fixture(autouse=True, scope="session")
def setup():
    connPool = asyncio.run(RedisClient().connect())
    yield connPool
    connPool.disconnect()


@pytest.mark.asyncio
async def test_basic_cache():
    DATA = "Hello World!"
    cache = XeltCache()
    key = CommandKeyBuilder(id=None, command=None)
    await cache.setBasicCache(value=DATA)
    assert await cache.getBasicCache(key) == DATA  # nosec


@pytest.mark.asyncio
async def test_basic_cache_type():
    DATA = "Hello World!"
    cache = XeltCache()
    key = CommandKeyBuilder(id=None, command=None)
    await cache.setBasicCache(value=DATA)
    assert isinstance(await cache.getBasicCache(key), str)  # nosec
