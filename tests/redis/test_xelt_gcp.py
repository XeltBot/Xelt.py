import sys
from pathlib import Path

from redis.asyncio.connection import ConnectionPool

path = Path(__file__).parents[2].joinpath("bot")
sys.path.append(str(path))

from bot.libs.cache import xeltCP


def test_get_cp():
    connPool = xeltCP.getConnPool()
    assert isinstance(connPool, ConnectionPool)


def test_creation_cp():
    connPool = xeltCP.createConnPool()
    assert isinstance(connPool, ConnectionPool)
