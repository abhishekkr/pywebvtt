from enum import Enum
import re
from .timestamp import parse_timestr, parse_timestamp

__all__ = ['Scene']


RegHeader = r"^\s*WEBVTT\s*"
RegNote = r"^\s*NOTE\s"
RegTimestamp = r'^\s*[0-9\:.]+\s*[\-+>\s*[0-9\:\.]+\s*$'


class Metadata(Enum):
    Discard = 0
    Header = 1
    Note = 2
    TimeRange = 3
    Subtext = 4


def parse(str):
    if str == "":
        return Metadata.Discard, None
    elif is_header(str):
        return Metadata.Header, None
    elif is_note(str):
        return Metadata.Note, None
    elif is_timestamp(str):
        start, end = parse_timestr(str)
        return Metadata.TimeRange, Scene(start=start, end=end)
    return Metadata.Subtext, None


def is_header(str):
    return (True if re.search(RegHeader, str) else False)


def is_note(str):
    return (True if re.search(RegNote, str) else False)


def is_timestamp(str):
    return (True if re.search(RegTimestamp, str) else False)


class Scene:
    def __init__(self, start='', end='', transcript=[], sub_type='vtt'):
        self.start = start
        self.end = end
        self.transcript = transcript
        self.sub_type = sub_type
        self._to_milliseconds_()

    def add_transcript(self, txt):
        self.transcript.append(txt)

    def _to_milliseconds_(self):
        self.start_millisec = parse_timestamp(self.start)
        self.end_millisec = parse_timestamp(self.end)
