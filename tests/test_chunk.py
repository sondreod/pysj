import pytest
from pytest import approx

from pysj import chunk


def test_chunking_of_string():
    assert list(chunk(4, "my test string is a multiple of 4...")) == [
        ("m", "y", " ", "t"),
        ("e", "s", "t", " "),
        ("s", "t", "r", "i"),
        ("n", "g", " ", "i"),
        ("s", " ", "a", " "),
        ("m", "u", "l", "t"),
        ("i", "p", "l", "e"),
        (" ", "o", "f", " "),
        ("4", ".", ".", "."),
    ]


def test_chunk_with_default_fill_value():
    assert list(chunk(4, range(10))) == [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, None, None)]


def test_chunk_with_fill_value():
    SENTINEL = object()
    assert list(chunk(4, range(6), SENTINEL)) == [
        (0, 1, 2, 3),
        (4, 5, SENTINEL, SENTINEL),
    ]
