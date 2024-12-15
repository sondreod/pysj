import datetime
import json
from collections import namedtuple
from dataclasses import dataclass

import pytest

from pysj import exjson, ndjson


@pytest.fixture
def test_json_data():
    decoded = [
        {"lol": 123},
        {"lol2": 123},
        {"lol3": 123},
        {"lol4": 123},
    ]

    # fmt: off
    encoded_ndjson = (
        '{"lol": 123}\n'
        '{"lol2": 123}\n'
        '{"lol3": 123}\n'
        '{"lol4": 123}'
    )
    # fmt: on

    TestData = namedtuple("TestData", "decoded encoded_ndjson")

    return TestData(decoded, encoded_ndjson)


def test_ndjson_encoding(test_json_data):
    assert test_json_data.encoded_ndjson == ndjson.dumps(test_json_data.decoded)


def test_ndjson_decoding(test_json_data):
    assert test_json_data.decoded == ndjson.loads(test_json_data.encoded_ndjson)


def test_ndjson_transcoding(test_json_data):
    assert test_json_data.decoded == ndjson.loads(ndjson.dumps(test_json_data.decoded))
