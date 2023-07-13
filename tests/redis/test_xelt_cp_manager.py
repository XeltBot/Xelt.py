import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

import pytest
from libs.cache import XeltCPM
from redis.asyncio.connection import ConnectionPool

REDIS_URI = "redis://localhost:6379/0"


@pytest.mark.asyncio
async def test_cpm():
    async with XeltCPM(uri=REDIS_URI) as cpm:
        assert isinstance(cpm, ConnectionPool)


def test_creation_cp():
    xeltCP = XeltCPM(uri=REDIS_URI)
    connPool = xeltCP.createPool()
    assert isinstance(connPool, ConnectionPool)


def test_get_cp():
    xeltCP = XeltCPM(uri=REDIS_URI)
    connPool = xeltCP.getConnPool()
    assert isinstance(connPool, ConnectionPool)


def test_created_cp():
    xeltCP = XeltCPM(uri=REDIS_URI)
    xeltCP.createPool()
    newConnPool = xeltCP.getConnPool()
    assert isinstance(newConnPool, ConnectionPool)
