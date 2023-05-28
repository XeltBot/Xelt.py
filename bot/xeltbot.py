import os

import asyncpg
import discord
from anyio import run
from dotenv import load_dotenv
from libs.utils import XeltLogger
from xeltcore import XeltCore

load_dotenv()

XELT_TOKEN = os.environ["XELT_DEV_TOKEN"]
POSTGRES_URI = os.environ["POSTGRES_URI"]
DEV_MODE = os.getenv("DEV_MODE") in ("True", "TRUE")

intents = discord.Intents.default()
intents.message_content = True


async def main():
    async with asyncpg.create_pool(
        POSTGRES_URI, command_timeout=60, max_size=20, min_size=20
    ) as pool:
        async with XeltCore(
            intents=intents, pool=pool, command_prefix="!", dev_mode=DEV_MODE
        ) as bot:
            await bot.start(XELT_TOKEN)


if __name__ == "__main__":
    try:
        with XeltLogger():
            run(main, backend_options={"use_uvloop": True})
    except KeyboardInterrupt:
        pass
