__version__ = '0.0.1'

from .webvtt import *
from .errors import *

__all__ = webvtt.__all__ + scene.__all__ + timestamp.__all__ + errors.__all__


def ParseFile(vttfile):
    return WebVTT(vttfile).parse_file()
