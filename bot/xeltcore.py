import logging
import os
from pathlib import Path
from typing import Optional

import discord
from discord.ext import commands


class XeltCore(commands.Bot):
    """Xelt.py's core"""

    def __init__(
        self,
        intents: discord.Intents,
        command_prefix: Optional[str] = "!",
        testing_guild_id: Optional[int] = None,
    ) -> None:
        super().__init__(intents=intents, command_prefix=command_prefix)
        self.testing_guild_id = testing_guild_id
        self.logger = logging.getLogger("discord")

    async def setup_hook(self) -> None:
        """The setup that is called before the bot is ready."""
        path = Path(__file__).parent
        cogs_path = path / "cogs"
        for cog in os.listdir(cogs_path):
            if cog.endswith(".py"):
                await self.load_extension(f"cogs.{cog[:-3]}")
                self.logger.debug(f"Loaded Cog: {cog[:-3]}")

        # This is needed in order to sync all of the commands to the testing guild.
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
