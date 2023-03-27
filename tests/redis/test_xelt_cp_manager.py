import sys
from pathlib import Path

from redis.asyncio.connection import ConnectionPool

path = Path(__file__).parents[2].joinpath("bot")
sys.path.append(str(path))

from bot.libs.cache import XeltCPManager


def test_create_cp():
    xeltCPM = XeltCPManager(host="localhost", port=6379)
    assert isinstance(xeltCPM.createConnPool(), ConnectionPool)


def test_get_cp():
    xeltCPM = XeltCPManager(host="localhost", port=6379)
    assert isinstance(xeltCPM.getConnPool(), ConnectionPool)


def test_get_cp_exists():
    xeltCPM = XeltCPManager(host="localhost", port=6379)
    xeltCPM.createConnPool()
    assert isinstance(xeltCPM.getConnPool(), ConnectionPool)
