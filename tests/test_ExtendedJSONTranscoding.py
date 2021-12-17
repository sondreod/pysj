import json
import datetime
import numpy as np

from pysj import ExtendedJSONEncoder, ExtendedJSONDecoder


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


def test_numpy_input():

    test = json.dumps(
        [1, 2, 3, np.int64(10), np.int8(11), np.int32(12)],
        cls=ExtendedJSONEncoder,
    )

    assert test == "[1, 2, 3, 10, 11, 12]"
