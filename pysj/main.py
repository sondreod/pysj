import dataclasses
import json
import math
import sys
import time
from datetime import date, datetime, timedelta
from fractions import Fraction
from itertools import cycle, islice, tee, zip_longest
from pathlib import Path
from typing import (Any, Callable, Iterable, List, Literal, Optional, Tuple,
                    Union)

from pysj import uuid

NUMPY_SUPPORT_FLAG = True
try:
    import numpy as np
except ImportError:
    NUMPY_SUPPORT_FLAG = False


class PythonVersion:
    def __init__(self, value=None):
        if not value:
            self.version = sys.version_info[:2]
        else:
            if isinstance(value, str):
                self.version = tuple(map(int, value.split(".")))
            elif isinstance(value, int):
                self.version = tuple(map(int, (str(value)[0], str(value)[1:])))
        self.version_string = ".".join(map(str, self.version))

    def __str__(self):
        return self.version_string

    def __int__(self):
        return self._convert_version_to_int(self.version_string)

    def __repr__(self):
        return f"{type(self)} {self.version_string}"

    def __eq__(self, other):
        return self.version == PythonVersion(other).version

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return self._convert_version_to_int(self) >= self._convert_version_to_int(other)

    def __gt__(self, other):
        return self._convert_version_to_int(self) > self._convert_version_to_int(other)

    def __le__(self, other):
        return self._convert_version_to_int(self) <= self._convert_version_to_int(other)

    def __lt__(self, other):
        return self._convert_version_to_int(self) < self._convert_version_to_int(other)

    @staticmethod
    def _convert_version_to_int(value):
        if not isinstance(value, PythonVersion):
            value = PythonVersion(value)
        return value.version[0] * 100 + value.version[1]


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
    Uses current time as default, can be overriden by setting *dt* to a datetime object.
    """
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


def months_in_interval(
    start: datetime,
    end: Optional[datetime] = None,
) -> Iterable[Tuple[int, int]]:
    """Yields months and year from the given interval (start -> end).

    start: datetime
        Start of interval
    end: datetime
        Optional, end of interval. Todays date is used if end is not set.

    return: Iterable[Tuple[int, int]]
    """
    if end is None:
        end = datetime.today()

    dt = datetime(start.year, start.month, 1)
    while dt <= datetime(end.year, end.month, 1):
        yield dt.month, dt.year

        dt = dt + timedelta(days=40)
        dt = datetime(dt.year, dt.month, 1)


def atomic_symlink(src: str, dst: str, raise_on_error=False):
    """Atomically creates a symlink *src* pointing to *dst*.

    Atomicity is achived trough renaming a temporary symlink with a random name.

    If *raise_on_error* is True and the rename failes, the original exception is raised.
    """

    tmp_link = Path("/tmp") / uuid()  # type: ignore

    tmp_link.symlink_to(dst)
    try:
        tmp_link.rename(src)  # Rename is atomic
    except Exception:  # If rename failes, remove tmp_file.
        tmp_link.unlink()
        if raise_on_error:
            raise


def flatten(iterable: Iterable) -> list:
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


def transpose(iterable: Iterable[Iterable]) -> List[List]:
    """Transpose a list of lists with dimensions X=Y."""

    return [list(x) for x in zip(*iterable)]


class ExtendedJSONEncoder(json.JSONEncoder):
    """Subclass for `json.JSONEncoder` making encoding of datetime, dataclasses and numpy arrays work.

    Usage
    -----
    >>> obj = {"timestamp": datetime.today()}
    >>> json.dumps(obj, cls=ExtendedJSONEncoder)

    """

    def default(self, o):
        # TODO: Support Decimal type
        if isinstance(o, datetime):
            return o.isoformat(timespec="seconds")
        if isinstance(o, date):
            return o.isoformat()
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
    def decoder(self):
        pass

    def encoder(self):
        pass


class NDJSONDecoder(json.JSONDecoder):
    def decode(self, s, *args, **kwargs):
        lines = ",".join(s.splitlines())
        text = f"[{lines}]"
        return super().decode(text, *args, **kwargs)


class NDJSONEncoder(json.JSONEncoder):
    def encode(self, o, *args, **kwargs):
        lines = []
        for el in o:
            line = super().encode(el, *args, **kwargs)
            lines.append(line)
        return "\n".join(lines)


class ExtendedNDJSONDecoder(NDJSONDecoder, ExtendedJSONDecoder):
    pass  # Gotta love Python, this is elegance :)


class ExtendedNDJSONEncoder(NDJSONEncoder, ExtendedJSONEncoder):
    pass


class EmptyError(BaseException):
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
        max_num_requests -= 1  # Zero indexed

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


def n_wise(n: int, data: Iterable):
    """Yields *n* items from data like a gliding window, as long as there is enough elements in data to yield the full window.
    If n == 3, and data = (1,2,3,4,5) the following items are yielded: (1,2,3), (2,3,4), (3,4,5).

    Like itertools.pairwise, but generalized to *n* items.
    """
    iterators = tee(
        data, n
    )  # Using tee on generators is not a good idéa if they are consumed very out of sync,  as all the intermidiate items must be cached.

    for i, iterator in enumerate(iterators):
        for _ in range(
            i
        ):  # But in this case the tee'd generators are never more out of sync than the length of the window (*n*)
            next(iterator, None)

    return zip(*iterators)


def triplewise(data: Iterable):
    return n_wise(3, data)


def moving_average(window_size: int, data: Iterable):
    yield from (sum(x) / window_size for x in n_wise(window_size, data))


def take(n: int, iterable: Iterable):
    """Return first n items of the *iterable*"""
    return islice(iterable, n)


SENTINEL = object()


def first(iterable: Iterable, empty_return_obj=SENTINEL):
    """Return first item of the *iterable*"""
    iterable_ = iter(iterable)
    try:
        return next(iterable_)
    except StopIteration:
        if empty_return_obj is not SENTINEL:
            return empty_return_obj
        else:
            raise EmptyError("Iterable passed to first() is empty.")


def chunk(n, iterable: Iterable, fillvalue=None):
    """Yields chunks of size *n* from *iterable*. Last chunk are filled with *fillvalue* if size of *iterable* is not a multiple of *n*."""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class Point:
    def __init__(
        self,
        x: int | float | None = None,
        y: int | float | None = None,
        z: int | float | None = None,
    ):
        self.x = x
        self.y = y
        self.z = z

        self.vector = tuple(s for s in [x, y, z] if s is not None)
        self.dimensions = self.axis = len(self.vector)

    def __str__(self):
        return f"Point({', '.join(map(str, self.vector))})"

    def __repr__(self):
        return self.__str__()

    def __abs__(self):
        return math.dist(tuple(0 for s in self.vector), self.vector)

    def __hash__(self):
        return hash(str(list(map(float, self.vector))))


def roundrobin(*iterables):
    """Yields elements from iterables in turn (roundrobin) until all is exhausted.

    Recipe credited to George Sakkis.
    From https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))
