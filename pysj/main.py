import json
from typing import Iterable, Callable, Any
from datetime import datetime
import typing

NUMPY_SUPPORT_FLAG = True
try:
    import numpy as np
except ImportError:
    NUMPY_SUPPORT_FLAG = False


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
    """Subclass for `json.JSONEncoder` making encoding of datetime and numpy arrays work.

    Usage
    -----
    >>> obj = {"timestamp": datetime.today()}
    >>> json.dumps(obj, cls=ExtendedJSONEncoder)

    """

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat(timespec="seconds")

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
                    d[k] = datetime.fromisoformat(v)
    return d


class ExtendedJSONDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=_extended_JSON_decoder_object_hook)


class ConfigurableJSONTranscoder:
    def decoder():
        pass

    def encoder():
        pass
