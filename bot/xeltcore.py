import logging
from pathlib import Path as SyncPath

import asyncpg
import discord
from cogs import EXTENSIONS
from discord.ext import commands
from libs.utils import check_db_servers
from libs.utils.help import XeltHelp
from redis.asyncio.connection import ConnectionPool

# Ripped off from Kumiko again
# Some weird import logic to ensure that watchfiles is there
_fsw = True
try:
    from watchfiles import awatch
except ImportError:
    _fsw = False


class XeltCore(commands.Bot):
    """Xelt.py's core"""

    def __init__(
        self,
        intents: discord.Intents,
        pool: asyncpg.Pool,
        redis_pool: ConnectionPool,
        command_prefix: str = "!",
        dev_mode: bool = False,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            intents=intents,
            command_prefix=command_prefix,
            help_command=XeltHelp(),
            *args,
            **kwargs,
        )
        self.dev_mode = dev_mode
        self._pool = pool
        self._redis_pool = redis_pool
        self.logger = logging.getLogger("xeltbot")

    @property
    def pool(self) -> asyncpg.Pool:
        """A global connection pool that is held throughout the lifetime of the bot

        Returns:
            asyncpg.Pool: Asyncpg connection pool
        """
        return self._pool

    @property
    def redis_pool(self) -> ConnectionPool:
        """A global redis connection pool that is held throughout the lifetime of the bot

        Returns:
            ConnectionPool: Redis connection pool
        """
        return self._redis_pool

    async def fsWatcher(self) -> None:
        cogsPath = SyncPath(__file__).parent.joinpath("Cogs")
        async for changes in awatch(cogsPath):
            changesList = list(changes)[0]
            if changesList[0].modified == 2:
                reloadFile = SyncPath(changesList[1])
                self.logger.info(f"Reloading extension: {reloadFile.name[:-3]}")
                await self.reload_extension(f"Cogs.{reloadFile.name[:-3]}")

    async def setup_hook(self) -> None:
        """The setup that is called before the bot is ready."""
        for cog in EXTENSIONS:
            self.logger.debug(f"Loaded Cog: {cog}")
            await self.load_extension(f"cogs.{cog}")

        self.loop.create_task(check_db_servers(self._pool, self._redis_pool))

        if self.dev_mode is True and _fsw is True:
            self.logger.info("Dev mode is enabled. Loading Jishaku and FSWatcher")
            self.loop.create_task(self.fsWatcher())
            await self.load_extension("jishaku")

    async def on_ready(self):
        currUser = None if self.user is None else self.user.name
        self.logger.info(f"{currUser} is fully ready!")
