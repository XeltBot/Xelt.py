import sys
from pathlib import Path

path = Path(__file__).parents[2]
sys.path.append(str(path))

from bot.libs.cache import CommandKeyBuilder


def test_key_builder_defaults():
    assert CommandKeyBuilder() == "cache:xeltpy:None:None"  # nosec


def test_key_builder_params():
    assert CommandKeyBuilder(id=123, command="test") == "cache:xeltpy:123:test"  # nosec


def test_key_builder_id():
    assert CommandKeyBuilder(id=123) == "cache:xeltpy:123:None"  # nosec
