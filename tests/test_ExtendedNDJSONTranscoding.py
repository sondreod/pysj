import datetime
import json
from dataclasses import dataclass

import numpy as np

from pysj import ExtendedNDJSONDecoder, ExtendedNDJSONEncoder


def test_date_ndjson_encoding():
    test = json.dumps(
        [
            {"lol": datetime.date(2023, 4, 6)},
            {"lol": datetime.date(2023, 4, 7)},
            {"lol": datetime.date(2023, 4, 8)},
            {"lol": datetime.date(2023, 4, 9)},
        ],
        cls=ExtendedNDJSONEncoder,
    )

    assert test == (
        '{"lol": "2023-04-06"}\n'
        '{"lol": "2023-04-07"}\n'
        '{"lol": "2023-04-08"}\n'
        '{"lol": "2023-04-09"}'
    )


def test_datetime_ndjson_encoding():
    test = json.dumps(
        [{"lol": datetime.datetime.fromisoformat("2021-12-01T04:50:00.123456")}],
        cls=ExtendedNDJSONEncoder,
    )

    assert test == '{"lol": "2021-12-01T04:50:00"}'


def test_datetime_ndjson_decoding():
    test = json.loads(
        '{"lol": "2021-12-01T04:50:00"}',
        cls=ExtendedNDJSONDecoder,
    )

    assert test == [{"lol": datetime.datetime.fromisoformat("2021-12-01T04:50:00")}]


def test_numpy_serialization():
    test = json.dumps(
        [1, 2, 3, np.int64(10), np.int8(11), np.int32(12)],
        cls=ExtendedNDJSONEncoder,
    )

    assert test == "1\n2\n3\n10\n11\n12"


def test_dataclass_serialization():
    @dataclass
    class TestDataClass:
        field_1: str
        field_2: int
        field_3: str

    test = json.dumps(
        [TestDataClass("lol", 1234, "kek")],
        cls=ExtendedNDJSONEncoder,
    )

    assert test == '{"field_1": "lol", "field_2": 1234, "field_3": "kek"}'
