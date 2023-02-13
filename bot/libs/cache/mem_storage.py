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
