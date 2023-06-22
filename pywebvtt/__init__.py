__version__ = '0.1.0'

from .webvtt import *
from .errors import *

__all__ = webvtt.__all__ + scene.__all__ + timestamp.__all__ + errors.__all__


def ParseFile(vttfile):
    return WebVTT(vttfile).parse_file()


def ParseFileWithOptions(vttfile, options):
    return WebVTT(vttfile, options=options).parse_file()


def Options(opts=None):
    if type(opts) != dict:
        return WebVTTOptions()
    if 'max_lines' not in opts.keys():
        if 'max_chars_per_line' not in opts.keys():
            return WebVTTOptions()
        else:
            return WebVTTOptions(max_chars_per_line=opts.max_chars_per_line)
    elif 'max_chars_per_line' not in opts.keys():
            return WebVTTOptions(max_lines=opts.max_lines)
    return WebVTTOptions(
        max_lines=opts.max_lines,
        max_chars_per_line=opts.max_chars_per_line,
    )
