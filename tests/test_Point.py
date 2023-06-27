import math
import sys

import pytest

if sys.version_info <= (3, 9):  # Point requires Python 3.10 or higher.
    from pysj import Point

    def test_1d():
        p = Point(1)
        assert p.dimensions == 1

    def test_3d():
        p = Point(1, 2, 3)
        assert p.dimensions == 3

    def test_distance_1d():
        a = Point(1)
        assert abs(a) == 1

    def test_distance_2d():
        a = Point(1, 1)
        assert abs(a) == math.sqrt(2)

    def test_distance_3d():
        a = Point(1, 2, 3)
        assert abs(a) == pytest.approx(3.74, abs=1e-2)

    def test_hash_ints():
        a = Point(2, 3, 4)
        b = Point(2, 3, 4)
        assert hash(a) == hash(b)

    def test_hash_mix_int_and_float():
        a = Point(1, 2.0, 3)
        b = Point(1.0, 2, 3.0)
        assert hash(a) == hash(b)

    def test_point_as_dict_key():
        my_point = {Point(13, 37): "exactly"}
