import datetime
import os
import platform
import time

import discord
import psutil
from discord.ext import commands
from xeltcore import XeltCore

BUILD_VERSION = "v3.0.0-dev"


class Meta(commands.Cog):
    """Provides metadata about Xelt"""

    def __init__(self, bot: XeltCore) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U00002754")

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()

    @commands.hybrid_command(name="support")
    async def support(self, ctx: commands.Context):
        """Need some help?"""
        embed = discord.Embed(color=discord.Color.from_rgb(133, 255, 159))
        embed.title = "Need some help?"
        embed.description = (
            "Feel free to join our server [here](https://discord.gg/e95ct6s5Gz)"
        )
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="invite")
    async def invite(self, ctx: commands.Context):
        """Invite me to your server!"""
        embed = discord.Embed(color=discord.Color.from_rgb(19, 191, 0))
        embed.title = "Invite me!"
        embed.description = "Want to invite Xelt to your own server?\nInvite me [here](https://discord.com/api/oauth2/authorize?client_id=726763157195849728&permissions=414501563457&scope=bot) and enjoy Xelt's features in your very own server!"
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="vote")
    async def vote(self, ctx: commands.Context):
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
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="stats")
    async def stats(self, ctx: commands.Context):
        """Show bot stats"""
        # Note that the calculation of the guilds and members may or may not take quite some time
        # discord.py should automatically cache how much guilds and members a bot is in
        uptime = datetime.timedelta(seconds=int(round(time.time() - startTime)))
        free_mem = psutil.virtual_memory().used / 1024 / 1024 / 1024
        total_mem = psutil.virtual_memory().total / 1024 / 1024 / 1024
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
            value=f"```💻 CPU [{os.cpu_count()} Cores]\n🎞 Memory [{free_mem:.2f} GB / {total_mem:.0f} GB] ```",
        )
        await ctx.send(embed=embed, ephemeral=True)


async def setup(bot: XeltCore) -> None:
    await bot.add_cog(Meta(bot))
