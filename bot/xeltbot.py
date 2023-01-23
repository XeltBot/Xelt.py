import logging
import os

import discord
from anyio import run
from dotenv import load_dotenv
from rich.logging import RichHandler
from xeltcore import XeltCore

# If there is an .env file, this will load them into the environment
load_dotenv()

# Add the constants here
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ["REDIS_PORT"])

# If the ID isn't set to a server, this will propagate the slash commands globally
DEV_GUILD = discord.Object(id=1057211769216569374)
XELT_TOKEN = os.environ["XELT_DEV_TOKEN"]
intents = discord.Intents.default()
intents.message_content = True

FORMATTER = logging.Formatter(fmt="%(message)s", datefmt="[%Y-%m-%d %H:%M:%S]")
HANDLER = RichHandler(show_path=False)
discord.utils.setup_logging(handler=HANDLER, formatter=FORMATTER)
logger = logging.getLogger("discord")


async def main():
    async with XeltCore(
        intents=intents,
        redis_host=REDIS_HOST,
        redis_port=REDIS_PORT,
        testing_guild_id=DEV_GUILD.id,
    ) as bot:
        await bot.start(XELT_TOKEN)


if __name__ == "__main__":
    try:
        run(main, backend_options={"use_uvloop": True})
    except KeyboardInterrupt:
        logger.info("Shutting down Xelt.py...")
