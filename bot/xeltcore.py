import logging
from typing import Optional

import discord
from anyio import Path
from discord.ext import commands


class XeltCore(commands.Bot):
    """Xelt.py's core"""

    def __init__(
        self,
        intents: discord.Intents,
        command_prefix: str = "!",
        testing_guild_id: Optional[int] = None,
    ) -> None:
        super().__init__(intents=intents, command_prefix=command_prefix)
        self.testing_guild_id = testing_guild_id
        self.logger = logging.getLogger("discord")

    async def setup_hook(self) -> None:
        """The setup that is called before the bot is ready."""
        cogsPath = Path(__file__).parent.joinpath("cogs")
        async for cog in cogsPath.rglob("*.py"):
            self.logger.debug(f"Loaded Cog: {cog.name[:-3]}")
            await self.load_extension(f"cogs.{cog.name[:-3]}")

        # This is needed in order to sync all of the commands to the testing guild.
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
