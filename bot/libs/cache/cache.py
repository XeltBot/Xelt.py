from typing import Optional, Union

import ormsgpack
from coredis import Redis
from utils import RedisClient

from .key_builder import CommandKeyBuilder


class XeltCache:
    """Xeltpy's custom caching utils. Uses Redis as the backend"""

    def __init__(self, host: str = "127.0.0.1", port: int = 6379) -> None:
        """Xeltpy's custom caching utils. Uses Redis as the backend

        Args:
            host (str, optional): Redis Host. Defaults to "127.0.0.1".
            port (int, optional): Redis Port. Defaults to 6379.
        """
        self.self = self
        self.host = host
        self.port = port

    async def setBasicCache(
        self,
        value: Union[str, bytes],
        key: str = CommandKeyBuilder(id=None, command=None),
        ttl: Optional[int] = 5,
    ) -> None:
        """Sets a basic cache to Redis. This is using the type `str` for the data type

        Args:
            value (Union[str, bytes]): The value to be stored in Redis
            key (Optional[str], optional): The key to be stored in Redis. Defaults to CommandKeyBuilder(id=None, command=None).
            ttl (Optional[int], optional): The time to live of the key. Defaults to 5.
        """
        connPool = RedisClient().getConnPool()
        conn = Redis(connection_pool=connPool)
        await conn.set(key=key, value=ormsgpack.packb(value), ex=ttl)

    async def getBasicCache(self, key: str) -> str:
        """Gets the basic command cache from Redis

        Args:
            key (str):

        Returns:
            str: _description_
        """
        conn = Redis(connection_pool=RedisClient().getConnPool())
        return ormsgpack.unpackb(await conn.get(key), option=ormsgpack.OPT_NON_STR_KEYS)  # type: ignore
