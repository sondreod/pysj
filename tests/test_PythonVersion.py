import sys

from pysj import PythonVersion


def test_to_str():
    assert str(PythonVersion(313)) == "3.13"


def test_to_int():
    assert int(PythonVersion("3.13")) == 313


def test_lt():
    assert PythonVersion(27) < 311


def test_qt():
    assert PythonVersion("3.12") > 311


def test_lte():
    assert PythonVersion(310) <= 310


def test_qte():
    assert PythonVersion("3.8") >= "2.7"


def test_equal():
    assert PythonVersion("3.11") == "3.11"


def test_not_equal():
    assert PythonVersion("3.11") != "3.12"
