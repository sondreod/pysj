import pytest

from pysj.formats import all_image_extensions, common_image_extensions


def test_common_formats():

    assert common_image_extensions == {
        "png",
        "jpg",
        "jpeg",
        "jfif",
        "j2p",
        "jpx",
        "j2k",
        "gif",
        "bmp",
        "dds",
        "dib",
        "eps",
        "icns",
        "im",
        "msp",
        "pcx",
        "apng",
        "pbm",
        "pgm",
        "ppm",
        "pnm",
        "sgi",
        "spi",
        "tga",
        "tiff",
        "tif",
        "webp",
        "xbm",
    }


def test_all_image_formats():
    len(all_image_extensions) >= 119
