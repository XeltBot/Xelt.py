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

from utils import RedisClient

load_dotenv(dotenv_path=envPath)


@pytest.mark.asyncio
async def test_create_redis_conn_pool():
    redisClient = await RedisClient().connect()
    assert isinstance(redisClient, ConnectionPool)  # nosec
