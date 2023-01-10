from typing import Union

from coredis import ConnectionPool


class RedisClient(object):
    """A wrapper class on top of Coredis's Redis client that implements a singleton design"""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 6379,
        max_connections: int = 25,
        db: int = 0,
    ):
        self.self = self
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.db = db
        self.shared_connection_pool = {"connPool": None}

    async def connect(self) -> ConnectionPool:
        """Connects to the Redis server, and automatically created a single connection pool

        Returns:
            coredis.ConnectionPool: The ConnectionPool class that can be used to access it
        """
        connPool = ConnectionPool(max_connections=self.max_connections).from_url(
            url=f"redis://@{self.host}:{self.port}/{self.db}?decode_responses=False"
        )
        self.shared_connection_pool = {"connPool": connPool}
        return connPool

    async def disconnect(self) -> None:
        """Closes all Redis connections in the pool"""
        self.shared_connection_pool["connPool"].disconnect()  # type: ignore

    def getConnPool(self) -> Union[ConnectionPool, None]:
        """Gets the current ConnectionPool obj

        Returns:
            Union[ConnectionPool, None]: Current `ConnectionPool` obj or None if not set
        """
        return self.shared_connection_pool["connPool"]
