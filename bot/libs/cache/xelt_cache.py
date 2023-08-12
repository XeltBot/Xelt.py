from typing import Any, Dict, Optional, Union

import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool

from .key_builder import command_key_builder


class XeltCache:
    """Xeltpy's custom caching utils. Uses Redis as the backend"""

    def __init__(self, connection_pool: ConnectionPool) -> None:
        """Xeltpy's custom caching utils. Uses Redis as the backend

        Args:
            connection_pool (ConnectionPool): The connection pool to use. This should be normally obtained from `RedisConnPoolCache.get_pool("_")`
        """
        self.self = self
        self.connection_pool: ConnectionPool = connection_pool

    def default_key(self, key: Optional[str]) -> str:
        """Determines whether to use the default `command_key_builder` str or not

        Args:
            key (Optional[str]): The key to be stored in Redis. Defaults to command_key_builder(id=None, command=None).

        Returns:
            str: The default key
        """
        if key is None:
            key = command_key_builder(id=None, command=None)
        return key

    async def set_basic_cache(
        self,
        key: Optional[str],
        value: Union[str, bytes] = "",
        ttl: Optional[int] = 30,
    ) -> None:
        """Sets the command cache on Redis
        Args:
            key (Optional[str], optional): Key to set on Redis. Defaults to `command_key_builder(prefix="cache", namespace="kumiko", user_id=None, command=None)`.
            value (Union[str, bytes, dict]): Value to set on Redis. Defaults to None.
            ttl (Optional[int], optional): TTL for the key-value pair. Defaults to 30.
        """
        default_key = command_key_builder(
            prefix="cache", namespace="kumiko", id=None, command=None
        )
        conn: redis.Redis = redis.Redis(connection_pool=self.connection_pool)
        await conn.set(
            name=key if key is not None else default_key, value=value, ex=ttl
        )
        await conn.close()

    async def get_basic_cache(self, key: str) -> Union[str, None]:
        """Gets the basic command cache from Redis

        Args:
            key (str): Redis key to look for. Consult `command_key_builder` for more info.

        Returns:
            Union[str, None]: The value of the key. If not found, returns `None`
        """
        conn: redis.Redis = redis.Redis(connection_pool=self.connection_pool)
        res = await conn.get(key)
        await conn.close()
        return res

    async def set_json_cache(
        self, key: str, value: Dict[str, Any], path: str = "$", ttl: int = 5
    ) -> None:
        """Sets the JSON cache on Redis

        Args:
            key (str): The key to use for Redis
            value (Dict[str, Any]): The value of the key-pair value
            path (str, optional): The path to use for the JSON. Defaults to "$".
            ttl (int, optional): TTL of the key-value pair. Defaults to 5.
        """
        client: redis.Redis = redis.Redis(connection_pool=self.connection_pool)
        await client.json().set(name=key, path=path, obj=value)
        await client.expire(name=key, time=ttl)
        await client.close()

    async def get_json_cache(self, key: str) -> Any:
        """Gets the JSON cache on Redis
        Args:
            key (str): The key of the key-value pair to get
        Returns:
            Any: The value of the key-value pair
        """
        client: redis.Redis = redis.Redis(connection_pool=self.connection_pool)
        value = await client.json().get(name=key)
        if value is None:
            await client.close(close_connection_pool=False)
            return None
        await client.close()
        return value

    async def cache_exists(self, key: str) -> bool:
        """Checks if the cache does exists

        Args:
            key (str): The key to use to search

        Returns:
            bool: `True` when the cache exists, `False` when it does not
        """
        client: redis.Redis = redis.Redis(connection_pool=self.connection_pool)
        res = await client.exists(key)
        await client.close()
        return True if res >= 1 else False
