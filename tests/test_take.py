import pytest
from pytest import approx

from pysj import take


def test_take_4():
    assert list(take(4, "abcdefgh")) == list("abcd")

def test_take_2():
    assert list(take(2, range(10))) == [0, 1]