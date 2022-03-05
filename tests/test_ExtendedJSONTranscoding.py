import datetime
import json
from dataclasses import dataclass

import numpy as np

from pysj import ExtendedJSONDecoder, ExtendedJSONEncoder


def test_datetime_json_encoding():

    test = json.dumps(
        {"lol": datetime.datetime.fromisoformat("2021-12-01T04:50:00.123456")},
        cls=ExtendedJSONEncoder,
    )

    assert test == '{"lol": "2021-12-01T04:50:00"}'


def test_datetime_json_decoding():

    test = json.loads(
        '{"lol": "2021-12-01T04:50:00"}',
        cls=ExtendedJSONDecoder,
    )

    assert test == {"lol": datetime.datetime.fromisoformat("2021-12-01T04:50:00")}


def test_numpy_serialization():

    test = json.dumps(
        [1, 2, 3, np.int64(10), np.int8(11), np.int32(12)],
        cls=ExtendedJSONEncoder,
    )

    assert test == "[1, 2, 3, 10, 11, 12]"


def test_dataclass_serialization():
    @dataclass
    class TestDataClass:
        field_1: str
        field_2: int
        field_3: str

    test = json.dumps(
        TestDataClass("lol", 1234, "kek"),
        cls=ExtendedJSONEncoder,
    )

    assert test == '{"field_1": "lol", "field_2": 1234, "field_3": "kek"}'
