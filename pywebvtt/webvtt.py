import os
import codecs

from .errors import MissingFileError, BadDataError
from . import scene

__all__ = ['WebVTT']


class WebVTT(object):
    """
    Parse subtitles from file in WebVTT format.
    To parse:
        WebVTT().ParseFile('sample.vtt')
    """

    def __init__(self, vttfile=''):
        self.vttfile = vttfile
        self.current_scene = None
        self.scenes = []

    def parse_file(self):
        if not os.path.exists(self.vttfile):
            raise MissingFileError("Missing File: %s" % self.vttfile)
        encoding = self._get_file_encoding_(self.vttfile)
        try:
            with open(self.vttfile, encoding=encoding) as f:
                for line in f.readlines():
                    self.parse_line(line)
                self._merge_current_scene_()
        except Exception as e:
            print(e)
            raise BadDataError("Error reading VTT file: %s" % self.vttfile)
        return self.scenes

    def parse_line(self, line):
        line = line.rstrip('\n\r')
        line_type, line_obj = scene.parse(line)
        if line_type == scene.Metadata.TimeRange:
            if self.current_scene is not None:
                self._merge_current_scene_()
            self.current_scene = line_obj
        elif line_type == scene.Metadata.Subtext:
            self.current_scene.add_transcript(line)

    def _merge_current_scene_(self):
        self.scenes.append(self.current_scene)

    def _get_file_encoding_(self, file_path):
        first_bytes = min(32, os.path.getsize(file_path))
        with open(file_path, 'rb') as f:
            raw = f.read(first_bytes)
        if raw.startswith(codecs.BOM_UTF8):
            return 'utf-8-sig'
        else:
            return 'utf-8'
