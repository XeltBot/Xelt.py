import discord
from discord.ext import commands
from xeltcore import XeltCore


class EventsHandler(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: XeltCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        exists_query = "SELECT EXISTS(SELECT 1 FROM guild WHERE id = $1);"
        insert_query = """
        WITH guild_insert AS (
            INSERT INTO guild (id) VALUES ($1)
        )
        INSERT INTO logging_config (guild_id) VALUES ($1);
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                exists = await conn.fetchval(exists_query, guild.id)
                if exists is False:
                    await conn.execute(insert_query, guild.id)
                    self.bot.prefixes.pop(guild.id, None)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        query = """
        DELETE FROM guild WHERE id=$1;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, guild.id)
            if guild.id in self.bot.prefixes:
                self.bot.prefixes[guild.id] = [self.bot.default_prefix]


async def setup(bot: XeltCore) -> None:
    await bot.add_cog(EventsHandler(bot))
