import pytest
from pytest import approx

from pysj import first


def test_first():
    assert first("ABCDE") == "A"

def test_first_tuple():
    assert first((1,2,3)) == 1