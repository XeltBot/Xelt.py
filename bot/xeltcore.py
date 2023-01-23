import logging
from typing import Optional

import discord
from anyio import Path
from discord.ext import commands
from redis.asyncio.connection import Connection, ConnectionPool

from bot.libs.cache import RedisConnPoolCache


class XeltCore(commands.Bot):
    """Xelt.py's core"""

    def __init__(
        self,
        intents: discord.Intents,
        command_prefix: str = "!",
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        testing_guild_id: Optional[int] = None,
    ) -> None:
        super().__init__(intents=intents, command_prefix=command_prefix)
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.testing_guild_id = testing_guild_id
        self.logger = logging.getLogger("xeltbot")

    async def setupRedisConnPool(self, key: str = "main") -> None:
        """Sets up the Redis connection pool"""
        conn = Connection(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        memCache = RedisConnPoolCache()
        await memCache.addConnPool(key=key, conn_pool_obj=ConnectionPool(connection_class=conn))  # type: ignore
        self.logger.info("Saved Redis connection pool into memory")

    async def setup_hook(self) -> None:
        """The setup that is called before the bot is ready."""
        cogsPath = Path(__file__).parent.joinpath("cogs")
        async for cog in cogsPath.rglob("*.py"):
            self.logger.debug(f"Loaded Cog: {cog.name[:-3]}")
            await self.load_extension(f"cogs.{cog.name[:-3]}")

        # Internally creates and saves the ConnectionPool object into memory
        # Now that ConnectionPool object can be used to access the Redis database
        await self.setupRedisConnPool()

        # This is needed in order to sync all of the commands to the testing guild.
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
