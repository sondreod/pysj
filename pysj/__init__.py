""" Pysj makes Python development more comfortable. This package contains utils, classes and helper
functions I find myself reimplementing in several projects."""
__version__ = "0.1a0"

from .main import ExtendedJSONEncoder, flatten
from .crypto import sha256, sha1, md5, uuid
