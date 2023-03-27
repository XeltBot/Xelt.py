import logging
import os

import discord
from anyio import run
from dotenv import load_dotenv

from bot.xeltcore import XeltCore

# If there is an .env file, this will load them into the environment
load_dotenv()

# If the ID isn't set to a server, this will propagate the slash commands globally
XELT_TOKEN = os.environ["XELT_DEV_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True

FORMATTER = logging.Formatter(
    fmt="%(asctime)s %(levelname)s    %(message)s", datefmt="[%Y-%m-%d %H:%M:%S]"
)
discord.utils.setup_logging(formatter=FORMATTER)
logger = logging.getLogger("discord")


async def main():
    async with XeltCore(
        intents=intents,
        command_prefix="!",
    ) as bot:
        await bot.start(XELT_TOKEN)


if __name__ == "__main__":
    try:
        run(main, backend_options={"use_uvloop": True})
    except KeyboardInterrupt:
        logger.info("Shutting down Xelt.py...")
