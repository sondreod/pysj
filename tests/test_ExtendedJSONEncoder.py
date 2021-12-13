import json
import datetime

from pysj import ExtendedJSONEncoder


def test_datetime_json_encoding():

    test = json.dumps(
        {"lol": datetime.datetime.fromisoformat("2021-12-01T04:50:00.123456")},
        cls=ExtendedJSONEncoder,
    )

    assert test == '{"lol": "2021-12-01T04:50:00"}'
