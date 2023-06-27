import sys

from pysj import PythonVersion, py


def test_system_version():
    assert PythonVersion() == ".".join(map(str, sys.version_info[:2])) == py


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
