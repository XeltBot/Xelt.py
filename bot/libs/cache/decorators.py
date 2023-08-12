import uuid
from functools import wraps
from typing import Any, Callable, Optional

from redis.asyncio.connection import ConnectionPool

from .key_builder import command_key_builder
from .xelt_cache import XeltCache


def cached(
    connection_pool: ConnectionPool,
    command_key: Optional[str],
    ttl: int = 30,
) -> Callable[..., Any]:
    """A decorator to cache the result of a function that returns a `str` to Redis.

    **Note**: The return type of the corountine used has to be `str` or `bytes`

    Args:
        connection_pool (ConnectionPool): Redis connection pool to use
        command_key (Optional[str]): Command key to use
        ttl (int, optional): TTL (Time-To-Live). Defaults to 30.

    Returns:
        Callable[..., Any]: The wrapper function
    """

    def wrapper(func: Callable[..., Any]) -> Any:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> Any:
            curr_func = await func(*args, **kwargs)
            cache = XeltCache(connection_pool=connection_pool)
            key = (
                command_key_builder(id=uuid.uuid4(), command=cached.__name__)
                if command_key is None
                else command_key
            )
            if await cache.cache_exists(key=key) is False:
                await cache.set_basic_cache(key=key, value=curr_func, ttl=ttl)
            else:
                return await cache.get_basic_cache(key=key)
            return curr_func

        return wrapped

    return wrapper


def cached_json(
    connection_pool: ConnectionPool,
    command_key: Optional[str],
    ttl: int = 30,
) -> Callable[..., Any]:
    """A decorator to cache the result of a function that returns a `dict` to Redis.

    **Note**: The return type of the corountine used has to be `dict`

    Args:
        connection_pool (ConnectionPool): Redis connection pool to use
        command_key (Optional[str]): Command key to use
        ttl (int, optional): TTL (Time-To-Live). Defaults to 30.

    Returns:
        Callable[..., Any]: The wrapper function
    """

    def wrapper(func: Callable[..., Any]) -> Any:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> Any:
            curr_func = await func(*args, **kwargs)
            if curr_func is None:
                return None
            cache = XeltCache(connection_pool=connection_pool)
            key = (
                command_key_builder(id=uuid.uuid4(), command=cached_json.__name__)
                if command_key is None
                else command_key
            )
            if await cache.cache_exists(key=key) is False:
                await cache.set_json_cache(key=key, value=curr_func, ttl=ttl)
            else:
                return await cache.get_json_cache(key=key)
            return curr_func

        return wrapped

    return wrapper
