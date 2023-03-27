import os
from pathlib import Path

from dotenv import load_dotenv
from libs.cache import XeltCPManager

path = Path(__file__).parents[2].joinpath(".env")

load_dotenv(dotenv_path=path)

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]

xeltCP: XeltCPManager = XeltCPManager(host=REDIS_HOST, port=int(REDIS_PORT))
