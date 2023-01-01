import datetime
import os
import platform
import time

import discord
import psutil
from discord import app_commands
from discord.ext import commands

BUILD_VERSION = "v3.0.0-dev"


class Xelt(commands.Cog):
    """Get Xelt to your server!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()

    @app_commands.command(name="support")
    async def getSupport(self, interaction: discord.Interaction):
        """Need some help?"""
        embed = discord.Embed(color=discord.Color.from_rgb(133, 255, 159))
        embed.title = "Need some help?"
        embed.description = (
            "Feel free to join our server [here](https://discord.gg/e95ct6s5Gz)"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="invite")
    async def getInvite(self, interaction: discord.Interaction):
        """Invite me to your server!"""
        embed = discord.Embed(color=discord.Color.from_rgb(19, 191, 0))
        embed.title = "Invite me!"
        embed.description = "Want to invite Xelt to your own server?\nInvite me [here](https://discord.com/api/oauth2/authorize?client_id=726763157195849728&permissions=414501563457&scope=bot) and enjoy Xelt's features in your very own server!"
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="vote")
    async def getVote(self, interaction: discord.Interaction):
        """Vote our bot!"""
        embed = discord.Embed(color=discord.Color.from_rgb(255, 145, 244))
        embed.title = "Vote us!"
        embed.description = "Help Xelt grow faster and reach many people by upvoting it on the following links!"
        embed.add_field(
            name="Top.gg", value="[Click here](https://top.gg/bot/726763157195849728)"
        )
        embed.add_field(
            name="Discord Bot List",
            value="[Click here](https://discordbotlist.com/bots/xelt)",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="stats")
    async def getStats(self, interaction: discord.Interaction):
        """Show bot stats"""
        # Note that the calculation of the guilds and members may or may not take quite some time
        # discord.py should automatically cache how much guilds and members a bot is in
        uptime = datetime.timedelta(seconds=int(round(time.time() - startTime)))
        freeMemory = psutil.virtual_memory().used / 1024 / 1024 / 1024
        totalMemory = psutil.virtual_memory().total / 1024 / 1024 / 1024
        embed = discord.Embed(
            title="Xelt's stats", description=f"```{BUILD_VERSION}```"
        )
        embed.add_field(name="Guilds", value=f"```{len(self.bot.guilds)}```")
        embed.add_field(name="Members", value=f"```{len(self.bot.users)}```")
        embed.add_field(
            name="Uptime",
            value=f"```{uptime.days} Days, {uptime.seconds//3600}:{(uptime.seconds//60)%60}:{(uptime.seconds%60)}```",
        )
        embed.add_field(name="Ping", value=f"```{self.bot.latency*1000:.2f}ms```")
        embed.add_field(name="discord.py version", value=f"```{discord.__version__}```")
        embed.add_field(
            name="Python Version", value=f"```{platform.python_version()}```"
        )
        embed.add_field(
            name="System",
            value=f"```💻 CPU [{os.cpu_count()} Cores]\n🎞 Memory [{freeMemory:.2f} GB / {totalMemory:.0f} GB] ```",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Xelt(bot))
