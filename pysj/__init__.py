""" Pysj makes Python development more comfortable, with utils, classes and helper
functions I find myself reimplementing in several projects."""
__version__ = "1.0.2"

from .crypto import md5, sha1, sha256, uuid
from .main import (ExtendedJSONDecoder, ExtendedJSONEncoder, Point,
                   PythonVersion, Timer, chunk, first, flatten, isotime,
                   months_in_interval, moving_average, n_wise, paginate, py,
                   seconds, take, transpose, triplewise)
