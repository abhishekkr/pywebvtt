import os
import codecs
import math

from .errors import MissingFileError, BadDataError
from . import scene

__all__ = ['WebVTTOptions', 'WebVTT']


class WebVTTOptions(object):
    """WebVTT parsing options.

    Attributes
    ----------
        max_lines : int
            maximum transcript lines to be used per scene
        max_chars_per_line : int
            maximum character per lines to be used in transcript
    """
    def __init__(self, max_lines=2, max_chars_per_line=16):
        self.max_lines = max_lines
        self.max_chars_per_line = max_chars_per_line


class WebVTT(object):
    """Parse subtitles from file in WebVTT format.
    To parse: WebVTT('sample.vtt').parse_file()

    Attributes
    ----------
        vttfile : str
            file path to vtt subtitle
        options : WebVTTOptions
            parsing options if need splitting scenes

    Methods
    -------
        parse_file():
            parse vttfile and assign read scenes to scenes, also return scenes
    """

    def __init__(self, vttfile='', options=None):
        self.vttfile = vttfile
        self.options = options
        self.current_scene = None
        self.scenes = []

    def parse_file(self):
        """Parses WebVTT subtitle file into Scenes with start/end timestamps
        and subtitle for that duration.

        Args: None

        Returns:
            A list of scenes parsed from vttfile.
        """
        if not os.path.exists(self.vttfile):
            raise MissingFileError("Missing File: %s" % self.vttfile)
        encoding = self._get_file_encoding_(self.vttfile)
        try:
            with open(self.vttfile, encoding=encoding) as f:
                for line in f.readlines():
                    self._parse_line_(line)
                self._merge_current_scene_()
        except Exception as e:
            print(e)
            raise BadDataError("Error reading VTT file: %s" % self.vttfile)
        return self.scenes

    def _parse_line_(self, line):
        line = line.rstrip('\n\r')
        line_type, line_obj = scene.parse(line)
        if line_type == scene.Metadata.TimeRange:
            if self.current_scene is not None:
                self._merge_current_scene_()
            self.current_scene = line_obj
        elif line_type == scene.Metadata.Subtext:
            self.current_scene.add_transcript(line)

    def _merge_current_scene_(self):
        if self.options == None:
            self.scenes.append(self.current_scene)
        else:
            self._merge_split_scene_()
            self.current_scene = None

    def _merge_split_scene_(self):
        duration_ms =  self.current_scene.duration_ms()
        transcript = self.current_scene.split_transcript(
            self.options.max_chars_per_line,
        )
        line_count = len(transcript)
        max_lines = self.options.max_lines
        new_scene_count = int(math.ceil(line_count / max_lines))
        split_duration = int(math.floor(duration_ms / new_scene_count))
        if line_count <= max_lines:
            self.current_scene.transcript = transcript
            self.scenes.append(self.current_scene)
            return
        start_ms = self.current_scene.start_millisec
        for idx in range(0, line_count, max_lines):
            end_ms = start_ms + split_duration
            if idx == line_count - 1:
                end_ms = self.current_scene.end_millisec
            start_ts = scene.millisec_to_timestamp(start_ms)
            end_ts = scene.millisec_to_timestamp(end_ms)
            new_scene = scene.Scene(start=start_ts, end=end_ts)
            new_scene.transcript = transcript[idx:(idx + max_lines)]
            self.scenes.append(new_scene)
            start_ms = end_ms

    def _get_file_encoding_(self, file_path):
        first_bytes = min(32, os.path.getsize(file_path))
        with open(file_path, 'rb') as f:
            raw = f.read(first_bytes)
        if raw.startswith(codecs.BOM_UTF8):
            return 'utf-8-sig'
        else:
            return 'utf-8'
