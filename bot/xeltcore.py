import logging

import discord
from anyio import Path
from discord.ext import commands

from bot.libs.utils.redis import redisCheck


class XeltCore(commands.Bot):
    """Xelt.py's core"""

    def __init__(
        self, intents: discord.Intents, command_prefix: str = "!", *args, **kwargs
    ) -> None:
        super().__init__(
            intents=intents, command_prefix=command_prefix, *args, **kwargs
        )
        self.logger = logging.getLogger("xeltbot")

    async def setup_hook(self) -> None:
        """The setup that is called before the bot is ready."""
        cogsPath = Path(__file__).parent.joinpath("cogs")
        async for cog in cogsPath.rglob("*.py"):
            self.logger.debug(f"Loaded Cog: {cog.name[:-3]}")
            await self.load_extension(f"cogs.{cog.name[:-3]}")

        self.loop.create_task(redisCheck())

    async def on_ready(self):
        currUser = None if self.user is None else self.user.name
        self.logger.info(f"{currUser} is fully ready!")
