import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2].joinpath("bot")
sys.path.append(str(path))

from libs.cache import cached, cached_json
from redis.asyncio.connection import ConnectionPool


@pytest.mark.asyncio
async def test_cache_deco():
    connPool = ConnectionPool(max_connections=25)

    @cached(connection_pool=connPool, command_key=None)
    async def testFunc():
        return "Hello World"

    res = await testFunc()
    assert (await testFunc() == "Hello World") and isinstance(res, str)  # nosec


@pytest.mark.asyncio
async def test_cache_deco_json():
    connPool = ConnectionPool(max_connections=25)

    @cached_json(connection_pool=connPool, command_key=None)
    async def testFuncJSON():
        return {"message": "Hello World"}

    res = await testFuncJSON()
    assert (await testFuncJSON() == {"message": "Hello World"}) and isinstance(  # nosec
        res, dict
    )
