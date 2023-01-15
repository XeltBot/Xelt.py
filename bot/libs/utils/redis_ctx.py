from contextlib import asynccontextmanager
from typing import AsyncGenerator

from .redis_utils import RedisClient


@asynccontextmanager
async def RedisPoolCM(
    host: str = "127.0.0.1", port: int = 6379, max_connections: int = 25, db: int = 0
) -> AsyncGenerator:
    """Async context manager that creates a Redis connection pool and closes it when done

    Args:
        host (str): The host to connect to. Defaults to "127.0.0.1"
        port (int): The port to connect to. Defaults to 6379
        max_connections (int): The maximum number of connections to create. Defaults to 25
        db (int): The database to connect to. Defaults to 0

    Returns:
        RedisClient: The RedisClient class that can be used to access the connection pool
    """
    redisClient = await RedisClient(
        host=host, port=port, max_connections=max_connections, db=db
    ).connect()
    try:
        yield redisClient
    finally:
        redisClient.disconnect()
