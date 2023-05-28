import os
from pathlib import Path

from dotenv import load_dotenv
from libs.cache import XeltCPManager

path = Path(__file__).parents[2].joinpath(".env")

load_dotenv(dotenv_path=path)

REDIS_URI = os.environ["REDIS_URI"]

xeltCP: XeltCPManager = XeltCPManager(uri=REDIS_URI)
