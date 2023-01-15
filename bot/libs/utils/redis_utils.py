import logging
from typing import Union

from coredis import ConnectionPool


class RedisClient:
    """A wrapper class on top of Coredis's Redis client that implements a singleton design"""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 6379,
        max_connections: int = 25,
        db: int = 0,
        *args,
        **kwargs,
    ):
        self.self = self
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.db = db
        self.conn_pool = ConnectionPool(*args, **kwargs)
        self.logger = logging.getLogger("discord")

    async def connect(self) -> ConnectionPool:
        """Connects to the Redis server, and automatically created a single connection pool

        Returns:
            coredis.ConnectionPool: The ConnectionPool class that can be used to access it
        """
        connPool = ConnectionPool(max_connections=self.max_connections).from_url(
            url=f"redis://@{self.host}:{self.port}/{self.db}?decode_responses=False"
        )
        self.conn_pool = connPool
        return connPool

    def disconnect(self) -> None:
        """Closes all Redis connections in the pool"""
        self.conn_pool.disconnect()

    def getConnPool(self) -> Union[ConnectionPool, None]:
        """Gets the current ConnectionPool obj

        Returns:
            Union[ConnectionPool, None]: Current `ConnectionPool` obj or None if not set
        """
        return self.conn_pool
