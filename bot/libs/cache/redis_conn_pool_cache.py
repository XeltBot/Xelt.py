from typing import List

from redis.asyncio.connection import ConnectionPool

from .base_cache import BaseRedisCache


class RedisConnPoolCache(BaseRedisCache):
    """Caching system used to internally cache Redis connection pools"""

    def __init__(self) -> None:
        super().__init__()

    async def setConnPool(self, key: str, conn_pool_obj: ConnectionPool) -> bool:
        """Sets a connection pool object in the cache

        Args:
            key (str): The key to set
            conn_pool_obj (ConnectionPool): The connection pool object to set

        Returns:
            bool: When the key has been successfully added
        """
        return await self._set(key=key, value=conn_pool_obj)

    async def addConnPool(self, key: str, conn_pool_obj: ConnectionPool) -> bool:
        """Adds a connection pool object in the cache

        Args:
            key (str): The key to set
            conn_pool_obj (ConnectionPool): The connection pool object to set

        Raises:
            ValueError: If the key is already in the cache

        Returns:
            bool: When the key has been successfully added
        """
        return await self._add(key=key, value=conn_pool_obj)

    async def doesKeyExist(self, key: str) -> bool:
        """Checks if a key exists in the cache

        Args:
            key (str): The key to check

        Returns:
            bool: If the key exists in the cache
        """
        return await self._exists(key=key)

    async def getConnPool(self, key: str) -> object:
        """Gets a connection pool object from the cache

        Args:
            key (str): The key to get

        Returns:
            ConnectionPool: The connection pool object
        """
        return await self._get(key=key)

    async def getAllConnPool(self) -> List[object]:
        """Gets all connection pool object from the cache

        Args:
            key (str): The key to get

        Returns:
            ConnectionPool: The connection pool object
        """
        return await self._listAll()

    async def deleteConnPool(self, key: str) -> bool:
        """Deletes a connection pool object from the cache

        Args:
            key (str): The key to delete

        Returns:
            bool: Whether it has been able to delete the key or not
        """
        return await self._delete(key=key)

    async def clearConnPool(self, namespace=None) -> bool:
        """Clears out the cache

        Args:
            namespace (str, optional): The namespace to clear. Defaults to None.
        """
        return await self._clear(namespace=namespace)
