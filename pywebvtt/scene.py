from enum import Enum
import math
import re

from .timestamp import parse_timestr, parse_timestamp
from .errors import BadTimestamp

__all__ = ['Metadata', 'Scene']


RegHeader = r"^\s*WEBVTT\s*"
RegNote = r"^\s*NOTE\s"
RegTimestamp = r'^\s*[0-9\:.]+\s+\-+>\s+[0-9\:\.]+\s*$'


class Metadata(Enum):
    """Metadata provides Enum for data types in VTT."""
    Discard = 0
    Header = 1
    Note = 2
    TimeRange = 3
    Subtext = 4


def parse(txt):
    """Parses WebVTT subtitle file into Scenes with start/end timestamps

    Args:
        txt : str
            line from subtitle file

    Returns:
        Returns tuple of VTT data type and any line object for it.
    """
    if txt == "":
        return Metadata.Discard, None
    elif is_header(txt):
        return Metadata.Header, None
    elif is_note(txt):
        return Metadata.Note, None
    elif is_timestamp(txt):
        start, end = parse_timestr(txt)
        return Metadata.TimeRange, Scene(start=start, end=end)
    return Metadata.Subtext, None


def is_header(txt):
    """Check if provided line is VTT Header.

    Args:
        txt : str
            line from subtitle file

    Returns:
        Returns bool for line is Header or not.
    """
    return re.search(RegHeader, txt) is not None


def is_note(txt):
    """Check if provided line is VTT Note.

    Args:
        txt : str
            line from subtitle file

    Returns:
        Returns bool for line is Note or not.
    """
    return re.search(RegNote, txt) is not None


def is_timestamp(txt):
    """Check if provided line is VTT Timestamp.

    Args:
        txt : str
            line from subtitle file

    Returns:
        Returns bool for line is Timestamp or not.
    """
    return re.search(RegTimestamp, txt) is not None


def millisec_to_timestamp(millisec):
    """Convert milliseconds to VTT timestamp format.

    Args:
        millisec : int
            Millisecond value indicator for Suntitle timestamp.

    Returns:
        Returns hh:mm:ss.ms format timestamp text for millisec provided.
    """
    try:
        milliseconds = int(millisec)
        seconds = math.floor(milliseconds / 1000)
        minutes = math.floor(seconds / 60)
        hours = math.floor(minutes / 60)
        if hours < 1:
            return "%02d:%02d.%03d" % (minutes % 60, seconds % 60, milliseconds % 1000)
        else:
            return "%02d:%02d:%02d.%03d" % (hours, minutes % 60, seconds % 60, milliseconds % 1000)
    except Exception as e:
        print(e)
        raise BadTimestamp("Failed to convert %s ms to timestamp." % str(millisec))


class Scene(object):
    """Scene to manage each block of time range with subtitle in it.
    To create:
        s = Scene(start='10.000', end='55.000')
    To add transcript for a scene:
        s.add_transcript('lorem ipsum')

    Attributes
    ----------
        start : str
            hh:mm:ss.ms format timestamp string for start of scene
        end : str
            hh:mm:ss.ms format timestamp string for end of scene

    Methods
    -------
        add_transcript(txt):
            add provided txt to scene's transcript
        string():
            return print-able text for scene
        sub_txt():
            return concatenated text from scene's transcript
        split_transcript(max_char_limit):
            return split transcript from current scene's transcript
            by provided max_char_limit
        duration_ms():
            return millisecond duration for current scene
        line_count():
            return number of transcript lines in current scene
        char_counts():
            return list of number of chars in transcript lines in current scene
        char_total():
            return total char count from current scene transcript
    """

    def __init__(self, start='', end=''):
        self.start = start
        self.end = end
        self.transcript = []
        self.sub_type = 'vtt'
        self._to_milliseconds_()

    def add_transcript(self, txt):
        """Add provided txt to scene's transcript.

        Args:
            txt : str
                transcript line to be added

        Returns: None
        """
        self.transcript.append(txt)

    def string(self):
        """Get print-able text for scene.

        Args: None

        Returns:
            A text representation for subtitle scene.
        """
        return """%s -> %s
%s
    """ % (self.start, self.end, self.sub_txt())

    def sub_txt(self):
        """Get concatenated text from scene's transcript.

        Args: None

        Returns:
            A concatenated text form of transcript.
        """
        strip_txt = [txt.strip().lstrip('-').strip() for txt in self.transcript]
        strip_txt = [txt.strip().lstrip('—').strip() for txt in strip_txt]
        return '\n'.join(strip_txt)

    def split_transcript(self, max_char_limit):
        """Get split transcript from current scene's transcript by char limit.

        Args: None

        Returns:
            A list of transcript with lines split by max char limit.
        """
        txt = self.sub_txt()
        return self._split_text_(txt, max_char_limit)

    def duration_ms(self):
        """Get millisecond duration for current scene.

        Args: None

        Returns:
            Millisecond count representating duration at which subtitle exists.
        """
        return self.end_millisec - self.start_millisec

    def line_count(self):
        """Get number of transcript lines in current scene.

        Args: None

        Returns:
            List of lines in per transcript.
        """
        return len(self.transcript)

    def char_counts(self):
        """Get list of char count in transcript lines in current scene.

        Args: None

        Returns:
            List of total number of characters per transcript line.
        """
        return [len(line) for line in self.transcript]

    def char_total(self):
        """Get total char count from current scene transcript.

        Args: None

        Returns:
            Total number of characters in transcript.
        """
        return sum(self.char_counts())

    def _to_milliseconds_(self):
        self.start_millisec = parse_timestamp(self.start)
        self.end_millisec = parse_timestamp(self.end)

    def _split_text_(self, text, max_char_limit):
        """Splits a text into a list of strings with a max character limit per item,
        while ensuring that each list item has full words.

        Args:
            text: The text to split.
            max_char_limit: The maximum number of characters per item.

        Returns:
            A list of strings.
        """
        items = []
        current_item = ''
        for w in text.split():
            if len(current_item + w) + 1 > max_char_limit:
                items.append(current_item)
                current_item = w
            else:
                current_item = w if current_item == '' else current_item + ' ' + w
        if current_item != '':
            items.append(current_item)
        return items
