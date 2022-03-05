from time import sleep

import pytest
from pytest import approx

from pysj import Timer


def test_lap_timing():

    timer = Timer()

    timer.start()
    for i in range(1, 4):
        print(i)
        sleep(0.1)
        assert timer.lap() == approx(i / 10, abs=1e-2)

    assert timer.total() == approx(0.3, abs=1e-2)


def test_reset_timing():

    timer = Timer()

    timer.start()
    for _ in range(1, 4):
        sleep(0.1)
        assert timer.reset() == approx(0.1, abs=1e-2)

    assert timer.total() == approx(0.3, abs=1e-2)


def test_use_as_contextmanager(capsys):

    with Timer():
        sleep(0.1)

    out, err = capsys.readouterr()
    output_line_1, output_line_2 = out.splitlines()
    assert output_line_1 == "Starting timer"
    assert output_line_2.startswith("Elapsed time")
    assert float(output_line_2[13:17]) == approx(0.1)
