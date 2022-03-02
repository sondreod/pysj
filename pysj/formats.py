# fmt: off
common_image_extensions = {  # Formats from the file support list of pillow
    "png", "jpg", "jpeg", "jfif", "j2p", "jpx", "j2k", "gif", "bmp", "dds", "dib", "eps", "icns", "im",
    "msp", "pcx", "apng", "pbm", "pgm", "ppm", "pnm", "sgi", "spi", "tga", "tiff", "tif", "webp", "xbm",
}

all_image_extensions = {
    'dwg', 'im', 'pti', 'tga', 'spng', 'emf', 'jxrs', 'dxf', 'tfx', 'cr2', 'jpg', 'dds', 'uvvi', 'webp',
    'jpe', 'avcs', 'cgm', 'ico', 'xpm', 'jxsc', 'b16', 'heic', 'wbmp', 'heif', 'rlc', 'fits', 'pgm',
    'hsj2', 'jph', 'jfif', 'jxss', 'jxr', 'avci', 'xwd', 'jxs', 'xif', 'svgz', 'hej2', 'svg', 'ppm',
    'dib', 'ktx2', 'jxsi', 'orf', 'jpgm', 'uvg', 'mdi', 'ief', 'jpg2', 'heics', 'pat', 'wmf', 's1n', 'uvi',
    'tiff', 'tif', 'ktx', 'sgi', 'jpf', 'mmr', 'apng', 'rgbe', 'fbs', 'pcx', 'uvvg', 'ras', 'fts', 'djvu',
    'xyze', 'xbm', 'sjpg', 'jp2', 'eps', 'cdr', 'j2k', 'sgif', 'azv', 'nef', 's1g', 'hdr', 'vtf', 'jpx',
    'jls', 'jxra', 'exr', 'btf', 'spi', 'psd', 'drle', 'msp', 'sjp', 'cdt', 'fst', 'erf', 'jng', 'bmp',
    'jpeg', 'jhc', 'crw', 'j2p', 'pnm', 'icns', 'fit', 'tap', 'fpx', 'jpm', 'cpt', 't38', 'heifs', 'jphc',
    'djv', 's1j', 'rgb', 'png', 'pgb', 'pbm', 'gif', 'btif', 'spn'}
# fmt: on


def _get_memetypes_from_os():
    """Todo: maybe use this in a build step"""
    import mimetypes

    mimetypes.init()
    for extension, mimetype in mimetypes.types_map.items():
        if mimetype.startswith("image/"):
            all_image_extensions.add(extension[1:].lower())
