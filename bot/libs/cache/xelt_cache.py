from typing import Any, Dict, Optional, Union

import ormsgpack
import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool

from .key_builder import CommandKeyBuilder


class XeltCache:
    """Xeltpy's custom caching utils. Uses Redis as the backend"""

    def __init__(self, connection_pool: ConnectionPool) -> None:
        """Xeltpy's custom caching utils. Uses Redis as the backend

        Args:
            connection_pool (ConnectionPool): The connection pool to use. This should be normally obtained from `RedisConnPoolCache.getConnPool("_")`
        """
        self.self = self
        self.connection_pool: ConnectionPool = connection_pool
        self.redisConn: redis.Redis = redis.Redis(connection_pool=self.connection_pool)

    def defaultKey(self, key: Optional[str]) -> str:
        """Determines whether to use the default `CommandKeyBuilder` str or not

        Args:
            key (Optional[str]): The key to be stored in Redis. Defaults to CommandKeyBuilder(id=None, command=None).

        Returns:
            str: The default key
        """
        if key is None:
            key = CommandKeyBuilder(id=None, command=None)
        return key

    async def setBasicCache(
        self,
        key: Optional[str],
        value: Union[str, bytes],
        ttl: Optional[int] = 5,
    ) -> None:
        """Sets a basic cache to Redis. This is using the type `str` for the data type

        Args:
            value (Union[str, bytes]): The value to be stored in Redis
            key (Optional[str], optional): The key to be stored in Redis. Defaults to CommandKeyBuilder(id=None, command=None).
            ttl (Optional[int], optional): The time (in seconds) that the key will exist. Basically the TTL. Defaults to 5.
        """
        await self.redisConn.set(
            name=self.defaultKey(key=key), value=ormsgpack.packb(value), ex=ttl
        )

    async def getBasicCache(self, key: str) -> Union[str, None]:
        """Gets the basic command cache from Redis

        Args:
            key (str): Redis key to look for. Consult `CommandKeyBuilder` for more info.

        Returns:
            Union[str, None]: The value of the key. If not found, returns `None`
        """
        getValue = await self.redisConn.get(key)
        if getValue is None:
            return None
        return ormsgpack.unpackb(getValue)  # type: ignore

    async def setJSONCache(self, key: str, value: Dict[str, Any], ttl: int = 5) -> None:
        """Sets the JSON cache on Redis
        Args:
            key (str): The key to use for Redis
            value (Dict[str, Any]): The value of the key-pair value
            ttl (Optional[int], optional): TTL of the key-value pair. Defaults to 5.
        """
        await self.redisConn.json().set(name=key, path="$", obj=value)
        await self.redisConn.expire(name=key, time=ttl)

    async def getJSONCache(self, key: str) -> Union[str, None]:
        """Gets the JSON cache on Redis
        Args:
            key (str): The key of the key-value pair to get
        Returns:
            Dict[str, Any]: The value of the key-value pair
        """
        value = await self.redisConn.json().get(name=key)
        if value is None:
            return None
        return value
