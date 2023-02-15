import asyncio
import logging
from typing import Optional

import discord
import redis.asyncio as redis
from anyio import Path
from discord.ext import commands
from prisma import Prisma  # type: ignore
from prisma.engine.errors import EngineConnectionError
from redis.asyncio.connection import ConnectionPool

from bot.libs.cache import globalMemStore
from bot.libs.utils import backoff


class XeltCore(commands.Bot):
    """Xelt.py's core"""

    def __init__(
        self,
        intents: discord.Intents,
        command_prefix: str = "!",
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        backoff_seconds: int = 5,
        testing_guild_id: Optional[int] = None,
    ) -> None:
        super().__init__(intents=intents, command_prefix=command_prefix)
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.backoff_seconds = backoff_seconds
        self.testing_guild_id = testing_guild_id
        self.logger = logging.getLogger("xeltbot")
        self.backoff_index = 0
        self.backoff_db_index = 0

    def setupRedisConnPool(self, key: str = "main") -> None:
        """Sets up the Redis connection pool"""
        conn = ConnectionPool.from_url(
            f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
        )
        globalMemStore.add(key=key, value=conn)
        self.logger.info("Saved Redis connection pool into memory")

    async def redisCheck(self, key: str = "main") -> None:
        """Checks if the Redis server is alive or not

        Args:
            key (str, optional): The key used to access the internal memory storage. Defaults to "main".
        """
        try:
            self.setupRedisConnPool(key=key)
            connPool = globalMemStore.get(key=key)
            r: redis.Redis = redis.Redis(connection_pool=connPool)
            res = await r.ping()
            isServerUp = True if res == b"PONG" or "PONG" else False
            self.logger.info(
                "Redis server is currently alive"
            ) if isServerUp else self.logger.error("Redis server is currently down")
        except ConnectionError:
            backoffTime = backoff(
                backoff_sec=self.backoff_seconds, backoff_sec_index=self.backoff_index
            )
            self.logger.error(
                f"Failed to connect to Redis server - Reconnecting in {int(backoffTime)} seconds"
            )
            await asyncio.sleep(backoffTime)
            self.backoff_index += 1
            await self.redisCheck()
        except TimeoutError:
            backoffTime = backoff(
                backoff_sec=self.backoff_seconds, backoff_sec_index=self.backoff_index
            )
            self.logger.error(
                f"Connection timed out - Reconnecting in {int(backoffTime)} seconds"
            )
            await asyncio.sleep(backoffTime)
            self.backoff_index += 1
            await self.redisCheck()

    async def connectDB(self) -> None:
        """Connects to the database"""
        try:
            db = Prisma(auto_register=True)
            await db.connect()
            self.logger.info("Successfully connected to the DB")
        except EngineConnectionError:
            backoffTime = backoff(backoff_sec=10, backoff_sec_index=self.backoff_index)
            self.logger.error("Failed to connect to the DB")
            await asyncio.sleep(backoffTime)
            self.backoff_db_index += 1
            await self.connectDB()

    async def setup_hook(self) -> None:
        """The setup that is called before the bot is ready."""
        # Load the cogs. The way how it's done is by recursively through the cogs folder
        cogsPath = Path(__file__).parent.joinpath("cogs")
        async for cog in cogsPath.rglob("*.py"):
            self.logger.debug(f"Loaded Cog: {cog.name[:-3]}")
            await self.load_extension(f"cogs.{cog.name[:-3]}")

        # Internally creates and saves the ConnectionPool object into memory
        # Now that ConnectionPool object can be used to access the Redis database
        # This will also ping the Redis server to make sure it is up
        self.loop.create_task(self.redisCheck(key="main"))
        self.loop.create_task(self.connectDB())

        # This is needed in order to sync all of the commands to the testing guild.
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
