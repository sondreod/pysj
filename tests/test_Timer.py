from pytest import approx
from pysj import Timer
from time import sleep


def test_lap_timing():

    timer = Timer()

    timer.start()
    for i in range(1, 4):
        print(i)
        sleep(1)
        assert timer.lap() == approx(i, abs=1e-2)

    assert timer.total() == approx(3, abs=1e-2)


def test_reset_timing():

    timer = Timer()

    timer.start()
    for _ in range(1, 4):
        sleep(1)
        assert timer.reset() == approx(1, abs=1e-2)

    assert timer.total() == approx(3, abs=1e-2)
