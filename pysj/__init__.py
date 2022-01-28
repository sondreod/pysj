""" Pysj makes Python development more comfortable, with utils, classes and helper
functions I find myself reimplementing in several projects."""
__version__ = "0.1a5"

from .main import (
    ExtendedJSONEncoder,
    ExtendedJSONDecoder,
    flatten,
    seconds,
    Timer,
    isotime,
)
from .crypto import sha256, sha1, md5, uuid
