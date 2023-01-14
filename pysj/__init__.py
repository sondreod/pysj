""" Pysj makes Python development more comfortable, with utils, classes and helper
functions I find myself reimplementing in several projects."""
__version__ = "0.1a15"

from .crypto import md5, sha1, sha256, uuid
from .main import (ExtendedJSONDecoder, ExtendedJSONEncoder, Timer, chunk,
                   flatten, isotime, moving_average, n_wise, paginate, seconds,
                   transpose, triplewise, take, first)
from .nanoservice import NanoService, NanoServiceClient
