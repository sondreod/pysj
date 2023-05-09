import pytest
from pytest import approx

from pysj import n_wise, triplewise

test_data = (1, 2, 3, 4, 5, 6)


def test_n_wise_2_comp_pairwise():
    try:
        from itertools import pairwise

        #  itertools.pairwise and n_wise with a n of 2 should be equal.
        assert sum(sum((a, b)) for a, b in pairwise(test_data)) == sum(
            sum((a, b)) for a, b in n_wise(2, test_data)
        )
    except ImportError:
        pass  # pairwise was added to itertools in Python 3.10


def test_n_wise_triplewise():
    assert sum(sum(t) for t in triplewise(test_data)) == 42


def test_n_wise_3():
    assert sum(sum(t) for t in n_wise(3, test_data)) == 42


def test_n_wise_4():
    assert sum(sum(t) for t in n_wise(4, test_data)) == 42


def test_n_wise_5():
    assert sum(sum(t) for t in n_wise(5, test_data)) == 35
