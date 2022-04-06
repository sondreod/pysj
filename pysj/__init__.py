""" Pysj makes Python development more comfortable, with utils, classes and helper
functions I find myself reimplementing in several projects."""
__version__ = "0.1a9"

from .crypto import md5, sha1, sha256, uuid
from .main import (ExtendedJSONDecoder, ExtendedJSONEncoder, Timer, flatten,
                   isotime, paginate, seconds)
from .nanoservice import NanoService, NanoServiceClient
