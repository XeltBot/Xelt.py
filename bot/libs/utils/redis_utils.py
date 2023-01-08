from coredis import Connection, ConnectionPool


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

    async def connect(self) -> ConnectionPool:
        """Connects to the Redis server, and automatically created a single connection pool

        Returns:
            coredis.ConnectionPool: The ConnectionPool class that can be used to access it
        """
        connDetails = Connection(
            host=self.host, port=self.port, db=self.db, decode_responses=False
        )
        connPool = ConnectionPool(
            connection_class=connDetails, max_connections=self.max_connections
        )
        return connPool
