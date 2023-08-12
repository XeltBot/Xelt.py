import logging

import asyncpg
import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool

logger = logging.getLogger("discord")


async def check_pg(pool: asyncpg.Pool) -> bool:
    """Ensures that the current connection pulled from the pool can be run.

    Args:
        conn_pool (asyncpg.Pool): The connection pool to get connections from.

    Returns:
        bool: True if the connection can be ran.
    """
    async with pool.acquire() as conn:
        status = conn.is_closed()
        if status is False:
            return True
    return False


async def check_redis(redis_pool: ConnectionPool):
    r: redis.Redis = redis.Redis(connection_pool=redis_pool)
    return await r.ping()


async def check_db_servers(pool: asyncpg.Pool, redis_pool: ConnectionPool) -> bool:
    """Ensures that the current connection pulled from the pool can be run for both PostgreSQL and Redis.

    Args:
        pool (asyncpg.Pool): Asyncpg connection pool
        redis_pool (ConnectionPool): Redis connection pool

    Returns:
        bool: True if the connection can be ran. False if both or one of them can't be ran.
    """
    logger = logging.getLogger("discord")
    if await check_pg(pool) is True:
        logger.info("PostgreSQL is up")
    if await check_redis(redis_pool) is True:
        logger.info("Redis is up")
    return True
