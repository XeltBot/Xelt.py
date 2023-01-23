import asyncio
from typing import Dict, List, Literal, Optional, Union

from redis.asyncio.connection import ConnectionPool


class BaseRedisCache:
    """Simple base for a cache backend

    This is based off of aiocache's backend caching
    """

    # Totally didn't rip the most of it off from aiocache
    def __init__(self) -> None:
        self._cache: Dict[str, ConnectionPool] = {}
        self._handlers: Dict[str, asyncio.TimerHandle] = {}

    async def _get(self, key: str) -> Union[ConnectionPool, None]:
        """Gets the value from a key in the internal memory cache

        Returns:
            Union[ConnectionPool, None]: If the key exists, it will return the `ConnectionPool` object.
            Otherwise it will return `None`
        """
        return self._cache.get(key)

    async def _getAll(self, keys: List[str]) -> List[Union[ConnectionPool, None]]:
        """Gets all the values from the internal memory cache

        Args:
            keys (List[str]): List of keys to get

        Returns:
            List[Union[ConnectionPool, None]]: List of `ConnectionPool` objects or `None`
        """
        return [self._cache.get(key) for key in keys]

    async def _listAll(self) -> List[ConnectionPool]:
        """Gets all the values from the internal memory cache

        Returns:
            List[ConnectionPool]: A list full of current connection pools
        """
        return list(self._cache.values())

    async def _set(self, key: str, value: ConnectionPool) -> Literal[True]:
        """Sets a key in the internal memory cache

        Args:
            key (str): The key to set
            value (ConnectionPool): The value to set

        Returns:
            Literal[True]: Always returns `True`, since it will always be set
        """
        self._cache[key] = value
        return True

    async def _add(self, key: str, value: ConnectionPool) -> Literal[True]:
        """Adds a key in the internal memory cache

        Args:
            key (str): The key to set
            value (ConnectionPool): `ConnectionPool` object to set

        Raises:
            ValueError: If the key is already in the cache

        Returns:
            Literal[True]: Always returns `True`, since it will always be set
        """
        if key in self._cache:
            raise ValueError(
                "Key {} already exists, use .set to update the value".format(key)
            )

        await self._set(key, value)
        return True

    async def _exists(self, key: str) -> bool:
        """Tests whether a key exists in the internal memory cache

        Args:
            key (str): The key to check against

        Returns:
            bool: Whether the key does exist within the internal cache
        """
        return key in self._cache

    async def _delete(self, key: str) -> bool:
        """Deletes a key from the internal memory cache

        Args:
            key (str): The key to delete

        Returns:
            bool: Whether it has been able to delete the key
        """
        return self.__delete(key)

    async def _clear(self, namespace: Optional[str]) -> Literal[True]:
        """Clears out the internal memory cache

        Args:
            namespace (str, optional): Namespace to clear. Defaults to None.

        Returns:
            bool: Confirmation that it has been cleared
        """
        if namespace:
            for key in list(self._cache):
                if key.startswith(namespace):
                    self.__delete(key)
        else:
            self._cache = {}
            self._handlers = {}
        return True

    def __delete(self, key: str) -> bool:
        """Internal method to delete a key

        Args:
            key (str): Given key

        Returns:
            bool: Whether it has been able to delete the key
        """
        if self._cache.pop(key, None) is not None:
            handle = self._handlers.pop(key, None)
            if handle:
                handle.cancel()
            return True
        return False
