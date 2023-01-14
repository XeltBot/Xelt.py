import os
import sys
from pathlib import Path

import pytest
from coredis import ConnectionPool
from dotenv import load_dotenv

path = Path(__file__).parents[2]
packagePath = os.path.join(str(path), "bot", "libs")
envPath = os.path.join(str(path), "bot", ".env")
sys.path.append(packagePath)

from utils import RedisClient, RedisPoolCM

load_dotenv(dotenv_path=envPath)


@pytest.mark.asyncio
async def test_create_redis_conn_pool():
    redisClient = await RedisClient().connect()
    assert isinstance(redisClient, ConnectionPool)  # nosec


@pytest.mark.asyncio
async def test_get_redis_ctx_conn():
    async with RedisPoolCM() as conn:
        assert isinstance(conn, ConnectionPool)  # nosec
