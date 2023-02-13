from asyncio import TimerHandle
from typing import Dict, Literal, Union

from redis.asyncio.connection import ConnectionPool


class MemStorage:
    """Simple memory storage to store objects

    *Note* : The expected `ConnectionPool` object comes from Redis's asyncio package
    """

    def __init__(self) -> None:
        self._storage: Dict[str, ConnectionPool] = {}
        self._handlers: Dict[str, TimerHandle] = {}

    def get(self, key: str) -> Union[ConnectionPool, None]:
        """Gets the value from a key in the internal memory storage

        Returns:
            Union[ConnectionPool, None]: If the key exists, it will return the value from it.
            Otherwise, it will return None
        """
        return self._storage.get(key)

    def set(self, key: str, value: ConnectionPool) -> Literal[True]:
        """Sets a key in the internal memory storage

        Args:
            key (str): The key to set
            value (ConnectionPool): The value to set (ConnectionPool)

        Returns:
            Literal[True] Always returns `True`, since it will always set it
        """
        self._storage[key] = value
        return True

    def add(self, key: str, value: ConnectionPool) -> Literal[True]:
        """Adds a key into the internal memory storage

        Args:
            key (str): The key to set
            value: (ConnectionPool): `ConnectionPool` object to set

        Raises:
            ValueError: If the key is already in the cache

        Returns:
            Literal[True]: Always returns `True`, since it will always be set
        """
        if key in self._storage:
            raise ValueError(f"Key {key} already exists, use .set to update the value")

        self.set(key, value)
        return True

    def exists(self, key: str) -> bool:
        """Tests whether a key exists in the internal memory storage

        Args:
            key (str): The key to check against

        Returns:
            bool: Whether the key does exist within the internal cache
        """
        return key in self._storage

    def delete(self, key: str) -> bool:
        """Deletes a key from the internal memory storage

        Args:
            key (str): The key to delete

        Returns:
            bool: Whether it has been able to delete the key
        """
        if self._storage.pop(key, None) is not None:
            handle = self._handlers.pop(key, None)
            if handle:
                handle.cancel()
            return True
        return False
