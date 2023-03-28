import logging
from pathlib import Path as SyncPath

import discord
from anyio import Path
from discord.ext import commands

from bot.libs.utils.redis import redisCheck

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
        command_prefix: str = "!",
        dev_mode: bool = False,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            intents=intents, command_prefix=command_prefix, *args, **kwargs
        )
        self.dev_mode = dev_mode
        self.logger = logging.getLogger("xeltbot")

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
        cogsPath = Path(__file__).parent.joinpath("cogs")
        async for cog in cogsPath.rglob("*.py"):
            self.logger.debug(f"Loaded Cog: {cog.name[:-3]}")
            await self.load_extension(f"cogs.{cog.name[:-3]}")

        if self.dev_mode is True and _fsw is True:
            self.logger.info("Dev mode is enabled. Loading Jishaku and FSWatcher")
            self.loop.create_task(self.fsWatcher())
            await self.load_extension("jishaku")
        self.loop.create_task(redisCheck())

    async def on_ready(self):
        currUser = None if self.user is None else self.user.name
        self.logger.info(f"{currUser} is fully ready!")
