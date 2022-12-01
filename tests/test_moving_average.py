import pytest

from pysj import moving_average

test_data = (1, 2, 3, 4, 5, 6)


def test_moving_average_2():
    assert tuple(moving_average(2, test_data)) == (1.5, 2.5, 3.5, 4.5, 5.5)


def test_moving_average_3():
    assert tuple(moving_average(3, test_data)) == (2, 3, 4, 5)


def test_moving_average_5():
    assert tuple(moving_average(5, test_data)) == (3, 4)
