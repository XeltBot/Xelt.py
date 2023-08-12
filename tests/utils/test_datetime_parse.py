import sys
from datetime import datetime, timezone
from pathlib import Path

path = Path(__file__).parents[2].joinpath("bot")
sys.path.append(str(path))

import pytest
from libs.utils import encode_datetime, parse_datetime


@pytest.fixture(scope="session", autouse=True)
def load_dict():
    return {"message": "Hello World", "created_at": datetime.now(tz=timezone.utc)}


def test_parse_date_obj():
    currDate = datetime.now(tz=timezone.utc)
    res = parse_datetime(datetime=currDate)
    assert isinstance(res, datetime)  # nosec


def test_parse_date_str():
    currDate = datetime.now(tz=timezone.utc).isoformat()
    res = parse_datetime(datetime=currDate)
    assert isinstance(res, datetime)  # nosec


def test_encode_datetime(load_dict):
    assert isinstance(encode_datetime(dict=load_dict)["created_at"], str)  # nosec
