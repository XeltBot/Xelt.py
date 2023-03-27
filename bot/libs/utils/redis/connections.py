import asyncio
import logging
from typing import Union

import redis.asyncio as redis
from libs.cache import xeltCP
from redis.asyncio.connection import ConnectionPool

from ..backoff_utils import backoff

logger = logging.getLogger("discord")


async def pingRedis(connection_pool: ConnectionPool) -> bool:
    """Checks whether the Redis server is up or not (via a PING/PONG request)

    Returns:
        bool: Whether the server is up or not
    """
    r: redis.Redis = redis.Redis(connection_pool=connection_pool)
    return await r.ping()


async def redisCheck(
    backoff_sec: int = 15, backoff_index: int = 0
) -> Union[bool, None]:
    """Recursive coroutine to continuously check if the Redis server is alive or not

    Note that there is a limit on how much it will check. The limit is 5 times.
    This is to prevent creating too much calls in the stack and by not doing so, the calls will not be cleaned up by the GC.

    Args:
        backoff_sec (int, optional): How much seconds to backoff. Defaults to 15.
        backoff_index (int, optional): Backoff index. Please don't adjust this. Defaults to 0.

    Returns:
        Union[bool, None]: Returns True if the server is up, False when the server cannot be contacted, and None when inside the recursive loop
    """
    try:
        connPool = xeltCP.getConnPool()
        res = await pingRedis(connection_pool=connPool)
        if backoff_index == 5:
            logger.error("Unable to connect to Redis server")
            return False
        if res is True:
            logger.info("Successfully connected to Redis server")
            return True
    except ConnectionError:
        backoffTime = backoff(backoff_sec=backoff_sec, backoff_sec_index=backoff_index)
        logger.error(
            f"Failed to connect to Redis server - Restarting connection in {int(backoffTime)} seconds"
        )
        await asyncio.sleep(backoffTime)
        await redisCheck(
            backoff_index=backoff_index + 1,
        )
