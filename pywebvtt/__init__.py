__version__ = '0.0.1'

from .webvtt import *
from .errors import *

__all__ = webvtt.__all__ + errors.__all__

ParseFile = WebVTT.ParseFile
