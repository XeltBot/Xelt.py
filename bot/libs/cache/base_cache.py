import asyncio
from typing import Dict, List, Optional


class BaseRedisCache:
    """Simple base for a cache backend

    This is based off of aiocache's backend caching
    """

    # Totally didn't rip the most of it off from aiocache
    def __init__(self) -> None:
        self._cache: Dict[str, object] = {}
        self._handlers: Dict[str, asyncio.TimerHandle] = {}

    async def _get(self, key: str) -> object:
        """Gets the value from a key in the internal memory cache

        Returns:
            object: The current object in the cache
        """
        return self._cache.get(key)

    async def _getAll(self, keys: List) -> List[object]:
        """Gets all the values from the internal memory cache

        Args:
            keys (List): List of keys to get

        Returns:
            List[object]: The list of objects to return
        """
        return [self._cache.get(key) for key in keys]

    async def _listAll(self) -> List[object]:
        """Gets all the values from the internal memory cache

        Args:
            keys (List): List of keys to get

        Returns:
            List[object]: The list of objects to return
        """
        return list(self._cache.values())

    async def _set(self, key: str, value: object) -> bool:
        """Sets a key in the internal memory cache

        Args:
            key (str): The key to set
            value (object): The value to set

        Returns:
            bool: Always returns `True`, since it will always be set
        """
        self._cache[key] = value
        return True

    async def _add(self, key: str, value: object) -> bool:
        """Adds a key in the internal memory cache

        Args:
            key (str): The key to set
            value (str): The value to set

        Raises:
            ValueError: If the key is already in the cache

        Returns:
            bool: When the key has been successfully added
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

    async def _clear(self, namespace: Optional[str]):
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
