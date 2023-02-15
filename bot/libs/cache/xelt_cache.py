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
        client: redis.Redis = redis.Redis(
            connection_pool=self.connection_pool, auto_close_connection_pool=False
        )
        await client.set(
            name=self.defaultKey(key=key), value=ormsgpack.packb(value), ex=ttl
        )
        await client.close(close_connection_pool=False)

    async def getBasicCache(self, key: str) -> Union[str, None]:
        """Gets the basic command cache from Redis

        Args:
            key (str): Redis key to look for. Consult `CommandKeyBuilder` for more info.

        Returns:
            Union[str, None]: The value of the key. If not found, returns `None`
        """
        client: redis.Redis = redis.Redis(
            connection_pool=self.connection_pool, auto_close_connection_pool=False
        )
        getValue = await client.get(key)
        if getValue is None:
            await client.close(close_connection_pool=False)
            return None
        await client.close(close_connection_pool=False)
        return ormsgpack.unpackb(getValue)  # type: ignore

    async def setJSONCache(
        self, key: str, value: Dict[str, Any], path: str = "$", ttl: int = 5
    ) -> None:
        """Sets the JSON cache on Redis

        Args:
            key (str): The key to use for Redis
            value (Dict[str, Any]): The value of the key-pair value
            path (str, optional): The path to use for the JSON. Defaults to "$".
            ttl (int, optional): TTL of the key-value pair. Defaults to 5.
        """
        client: redis.Redis = redis.Redis(
            connection_pool=self.connection_pool, auto_close_connection_pool=False
        )
        await client.json().set(name=key, path=path, obj=value)
        await client.expire(name=key, time=ttl)
        await client.close(close_connection_pool=False)

    async def getJSONCache(self, key: str) -> Any:
        """Gets the JSON cache on Redis
        Args:
            key (str): The key of the key-value pair to get
        Returns:
            Any: The value of the key-value pair
        """
        client: redis.Redis = redis.Redis(
            connection_pool=self.connection_pool, auto_close_connection_pool=False
        )
        value = await client.json().get(name=key)
        if value is None:
            await client.close(close_connection_pool=False)
            return None
        await client.close(close_connection_pool=False)
        return value

    async def cacheExists(self, key: str) -> bool:
        """Checks if the cache does exists

        Args:
            key (str): The key to use to search

        Returns:
            bool: `True` when the cache exists, `False` when it does not
        """
        client: redis.Redis = redis.Redis(
            connection_pool=self.connection_pool, auto_close_connection_pool=False
        )
        res = await client.exists(key)
        await client.close(close_connection_pool=False)
        return True if res >= 1 else False
