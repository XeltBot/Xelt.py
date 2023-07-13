import asyncio
import os

import asyncpg
import discord
import uvloop
from dotenv import load_dotenv
from libs.cache import XeltCPM
from libs.utils import XeltLogger
from xeltcore import XeltCore

load_dotenv()

XELT_TOKEN = os.environ["XELT_DEV_TOKEN"]
POSTGRES_URI = os.environ["POSTGRES_URI"]
REDIS_URI = os.environ["REDIS_URI"]
DEV_MODE = os.getenv("DEV_MODE") in ("True", "TRUE")

intents = discord.Intents.default()
intents.message_content = True


async def main():
    async with asyncpg.create_pool(
        dsn=POSTGRES_URI, command_timeout=60, max_size=20, min_size=20
    ) as pool, XeltCPM(uri=REDIS_URI, max_size=25) as redis_pool:
        async with XeltCore(
            intents=intents,
            pool=pool,
            redis_pool=redis_pool,
            command_prefix="!",
            dev_mode=DEV_MODE,
        ) as bot:
            await bot.start(XELT_TOKEN)


if __name__ == "__main__":
    try:
        with XeltLogger():
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
            asyncio.run(main())
    except KeyboardInterrupt:
        pass
