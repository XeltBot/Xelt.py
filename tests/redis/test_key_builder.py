import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("bot")
sys.path.append(str(path))

from libs.cache import command_key_builder


def test_key_builder_defaults():
    assert command_key_builder() == "cache:xeltpy:None:None"  # nosec


def test_key_builder_params():
    assert (
        command_key_builder(id=123, command="test") == "cache:xeltpy:123:test"
    )  # nosec


def test_key_builder_id():
    assert command_key_builder(id=123) == "cache:xeltpy:123:None"  # nosec
