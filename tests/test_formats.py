import pytest
from pysj import formats


def test_common_formats():

    assert formats.common_image_extensions == {
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
    len(formats.all_image_extensions) >= 119
