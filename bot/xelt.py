import logging
from pathlib import Path
from typing import Union

import asyncpg
import discord
from aiohttp import ClientSession
from cogs import EXTENSIONS, VERSION
from discord.ext import commands
from libs.utils.config import XeltConfig
from libs.utils.context import XeltContext
from libs.utils.errors import send_error_embed
from libs.utils.help import XeltHelp
from libs.utils.reloader import Reloader


class Xelt(commands.Bot):
    """Xelt's core"""

    def __init__(
        self,
        config: XeltConfig,
        intents: discord.Intents,
        session: ClientSession,
        pool: asyncpg.Pool,
        **kwargs,
    ):
        super().__init__(
            activity=discord.Activity(type=discord.ActivityType.watching, name="!help"),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, replied_user=False
            ),
            command_prefix=["?", "!"],
            help_command=XeltHelp(),
            intents=intents,
            **kwargs,
        )
        self.default_prefix = "!"
        self.session = session
        self.pool = pool
        self.logger = logging.getLogger("xelt")
        self.version = str(VERSION)
        self._dev_mode = config.xelt.get("dev_mode", False)
        self._reloader = Reloader(self, Path(__file__).parent)

    ### Bot-related overrides

    async def get_context(
        self, origin: Union[discord.Interaction, discord.Message], /, *, cls=XeltContext
    ) -> XeltContext:
        return await super().get_context(origin, cls=cls)

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        await send_error_embed(ctx, error)

    async def setup_hook(self) -> None:
        for extension in EXTENSIONS:
            await self.load_extension(extension)

        await self.load_extension("jishaku")

        if self._dev_mode:
            self.logger.info("Dev mode enabled. Enabling Reloader")
            self._reloader.start()

    async def on_ready(self) -> None:
        if not hasattr(self, "uptime"):
            self.uptime = discord.utils.utcnow()

        user = self.user.name if self.user is not None else None
        self.logger.info(f"{user} is fully ready!")
