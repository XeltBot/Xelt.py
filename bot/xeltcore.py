import logging
import signal
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
        self._prefixes = {}
        self.default_prefix = "!"
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

    @property
    def prefixes(self) -> dict[int, list[str]]:
        """A dictionary of prefixes for each guild

        Returns:
            dict[int, list[str]]: A dictionary of prefixes for each guild
        """
        return self._prefixes

    async def fs_watcher(self) -> None:
        cogs_path = SyncPath(__file__).parent.joinpath("Cogs")
        async for changes in awatch(cogs_path):
            changes_list = list(changes)[0]
            if changes_list[0].modified == 2:
                reload_file = SyncPath(changes_list[1])
                self.logger.info(f"Reloading extension: {reload_file.name[:-3]}")
                await self.reload_extension(f"cogs.{reload_file.name[:-3]}")

    async def setup_hook(self) -> None:
        """The setup that is called before the bot is ready."""

        def stop():
            self.loop.create_task(self.close())

        self.loop.add_signal_handler(signal.SIGTERM, stop)
        self.loop.add_signal_handler(signal.SIGINT, stop)
        for cog in EXTENSIONS:
            self.logger.debug(f"Loaded Cog: {cog}")
            await self.load_extension(cog)

        self.loop.create_task(check_db_servers(self._pool, self._redis_pool))

        if self.dev_mode is True and _fsw is True:
            self.logger.info("Dev mode is enabled. Loading Jishaku and fs_watcher")
            self.loop.create_task(self.fs_watcher())
            await self.load_extension("jishaku")

    async def on_ready(self):
        curr_user = None if self.user is None else self.user.name
        self.logger.info(f"{curr_user} is fully ready!")
