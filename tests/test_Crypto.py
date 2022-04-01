import string

import pytest

from pysj import md5, sha1, sha256, uuid
from pysj.crypto import ALPHABET


@pytest.mark.parametrize(
    "hash_algorithm, digest",
    [
        ("sha256", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"),
        ("sha1", "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3"),
        ("md5", "098f6bcd4621d373cade4e832627b4f6"),
    ],
)
def test_hashing(hash_algorithm, digest):
    assert eval(f"{hash_algorithm}('test')") == digest


def test_uuid_generation():
    assert len(uuid()) == 36 and all([x in string.hexdigits + "-" for x in uuid()])


def test_uuid_alpha_generation():
    assert 20 < len(uuid("alpha")) < 24 and all([x in ALPHABET for x in uuid("alpha")])


def test_uuid_int_generation():
    assert isinstance(uuid("int"), int)


def test_force_mutable():
    assert sha256([1, 2, 3], force_mutable=True) == sha256("[1, 2, 3]")


def test_force_mutable_error_when_flag_is_false():
    with pytest.raises(AttributeError):
        assert sha256([1, 2, 3])
