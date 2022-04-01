import dataclasses
import json
import time
from datetime import datetime, timedelta
from fractions import Fraction
from typing import Any, Callable, Iterable, Tuple

NUMPY_SUPPORT_FLAG = True
try:
    import numpy as np
except ImportError:
    NUMPY_SUPPORT_FLAG = False


class Timer:
    """Simple class working like a stopwatch."""

    def __init__(self) -> None:

        self.time = None
        self.start_time = time.perf_counter()

    def __enter__(self):
        print("Starting timer")
        self.start()

    def __exit__(self, *_):
        print("Elapsed time", self.lap(), "s.")

    def start(self):
        self.time = time.perf_counter()

    def reset(self):
        end_time = self.lap()
        self.start()
        return end_time

    def lap(self):
        return time.perf_counter() - self.time

    def split(self):
        """Alias for lap"""
        return self.lap()

    def total(self):
        return time.perf_counter() - self.start_time


def isotime(precision="d", dt=None):
    """Get the current date/time in isoformat. Default precision is day, accepts d(ay), (h)our, (m)inute, (s)econd.
    Per defualt the current time is used, this can be overriden by supplying a datetime object with the *dt* kwarg"""
    if not dt:
        dt = datetime.now()
    precision_map = {
        "d": slice(0, 10),
        "h": slice(0, 13),
        "m": slice(0, 16),
        "s": slice(0, 19),
    }

    return dt.isoformat()[precision_map.get(precision[0])]


def seconds(
    days=0,
    seconds=0,
    microseconds=0,
    milliseconds=0,
    minutes=0,
    hours=0,
    weeks=0,
    years=0,
    months=0,
    quarters=0,
) -> int:
    """Returns the number of seconds in the given time intervals combined, rounded down to nearest integer.

    This is a short variant of `int(timedelta(**kwargs).total_seconds())` with a
    few extra named time intervals(year, month, quarter)

    A year is calculated as 365 days, a month is 30 days, a quarter is 1/4 of a year
    """

    days += float((Fraction(365, 4) * quarters))
    days += months * 30
    days += years * 365

    return int(
        timedelta(
            days, seconds, microseconds, milliseconds, minutes, hours, weeks
        ).total_seconds()
    )


def flatten(iterable: Iterable):
    """Recursively flattens an iterable (depth first)

    Usage
    -----

    >>> nested_list = [[(1.3, 3.0), "string", "another string"], [4, 5E2, sorted({"a", "b", "c"})]]
    >>> print(flatten(nested_list))
    [1.3, 3.0, "string", "another string", 4, 5E2, "a", "b", "c"]

    """

    def _recursively_flatten(iterable: Iterable):
        for e in iterable:
            if isinstance(e, Iterable) and not isinstance(e, str):
                yield from _recursively_flatten(e)
            else:
                yield e

    return list(_recursively_flatten(iterable))


class ExtendedJSONEncoder(json.JSONEncoder):
    """Subclass for `json.JSONEncoder` making encoding of datetime, dataclasses and numpy arrays work.

    Usage
    -----
    >>> obj = {"timestamp": datetime.today()}
    >>> json.dumps(obj, cls=ExtendedJSONEncoder)

    """

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat(timespec="seconds")
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)

        if NUMPY_SUPPORT_FLAG and type(o) in [np.int8, np.int16, np.int32, np.int64]:
            return int(o)

        return super().default(o)


def _extended_JSON_decoder_object_hook(d):
    for k, v in d.items():
        if isinstance(v, dict):
            _extended_JSON_decoder_object_hook(v)
        else:
            if isinstance(v, str):
                if any(
                    [
                        v.startswith("19"),
                        v.startswith("20"),
                    ]
                ):
                    try:
                        d[k] = datetime.fromisoformat(v)
                    except ValueError:
                        pass  # Invalid isoformat string, leave as is
    return d


class ExtendedJSONDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=_extended_JSON_decoder_object_hook)


class ConfigurableJSONTranscoder:
    def decoder():
        pass

    def encoder():
        pass


def paginate(
    url: str,
    pagesize=500,
    data_attribute_name=None,
    max_num_requests=10_000,
    start_one=False,
    offset_is_n_of_elements=False,
):
    """Function returning a function yielding new urls if the data seems valid

    Usage
    -----

        get_url = paginate("lol.lol?offset=OFFSET&pagesize=PAGESIZE", max_num_requests=20, start_one=False)

        data = None
        while url := get_url(data):
            data = requests.get(url)
            # Do someting with the data, get_url will yield a new url a long as data is set to
            # someting looking like a valid json response without an error attribute,
            # and as long the data don't repeat.

    """
    n = -1
    offset_multiplier = 1
    if offset_is_n_of_elements:
        offset_multiplier = pagesize

    if start_one:
        n = 0
    else:
        max_num_requests -= 1  #  Zero indexed

    last_response = "not_json"

    def inner_page(data=None):
        nonlocal n
        if (
            data := _extract_json_data(data, data_attribute_name)
            and n < max_num_requests
            and last_response != data
        ):
            n += 1
            return url.replace("OFFSET", str(n * offset_multiplier)).replace(
                "PAGESIZE", str(pagesize)
            )

    def _extract_json_data(data, data_attr=None):
        """Extracts and returns items in json response, or False if there are no more items, returns True if data is None"""

        if isinstance(data, dict):
            if data.get("error"):
                return False
            if data_attr:
                data = data.get(data_attr)
            else:
                if data.get("data"):
                    data = data.get("data")
                elif data.get("items"):
                    data = data.get("items")

        if data is None:
            return True
        elif data:
            return data
        else:
            return False

    return inner_page
