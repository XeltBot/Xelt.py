import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2].joinpath("bot")
sys.path.append(str(path))

from bot.libs.cache import XeltCPManager
from bot.libs.utils.redis import pingRedis, redisCheck


@pytest.mark.asyncio
async def test_ping_redis():
    xeltCPM = XeltCPManager(host="localhost", port=6379)
    assert await pingRedis(connection_pool=xeltCPM.getConnPool()) == True


@pytest.mark.asyncio
async def test_redis_check_success():
    assert await redisCheck() == True
