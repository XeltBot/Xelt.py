from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from xeltcore import XeltCore


class Typerace(commands.Cog):
    """Play the typerace game here!"""

    def __init__(self, bot: XeltCore) -> None:
        self.bot = bot

    @app_commands.command(name="typerace")
    @app_commands.describe(public="Whether the game is public or private")
    async def typeraceGame(
        self, interaction: discord.Interaction, public: Optional[bool] = True
    ) -> None:
        await interaction.response.send_message("testing")


async def setup(bot: XeltCore) -> None:
    await bot.add_cog(Typerace(bot))
