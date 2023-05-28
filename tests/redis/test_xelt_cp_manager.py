import sys
from pathlib import Path

from redis.asyncio.connection import ConnectionPool

path = Path(__file__).parents[2].joinpath("bot")
sys.path.append(str(path))

from libs.cache import XeltCPManager

REDIS_URI = "redis://localhost:6379/0"


def test_create_cp():
    xeltCPM = XeltCPManager(uri=REDIS_URI)
    assert isinstance(xeltCPM.createConnPool(), ConnectionPool)


def test_get_cp():
    xeltCPM = XeltCPManager(uri=REDIS_URI)
    assert isinstance(xeltCPM.getConnPool(), ConnectionPool)


def test_get_cp_exists():
    xeltCPM = XeltCPManager(uri=REDIS_URI)
    xeltCPM.createConnPool()
    assert isinstance(xeltCPM.getConnPool(), ConnectionPool)
