from enum import Enum
import re
from .errors import BadTimestamp

__all__ = ['TimeRangeType']


RegTimeHMSMs = r"^\s*([0-9]+)\:([0-9]+)\:([0-9]+)\.([0-9]+)\s*$"
RegTimeMSMs = r"^\s*([0-9]+)\:([0-9]+)\.([0-9]+)\s*$"
RegTimeSMs = r"^\s*([0-9]+)\.([0-9]+)\s*$"


class TimeRangeType(Enum):
    """TimeRangeType provides Enum for data types in Timestamp."""
    HMSMs = 1
    MSMs = 2
    SMs = 3


def get_time_range_type(txt):
    """Get time range type for time range line text.

    Args:
        txt : str
            'hh:mm:ss.ms' format timestamp text
            (hh for hours, mm for minutes, ss for seconds, ms for millisec)

    Returns:
        Timestamp data type.
    """
    if re.search(RegTimeHMSMs, txt):
        return TimeRangeType.HMSMs
    elif re.search(RegTimeMSMs, txt):
        return TimeRangeType.MSMs
    elif re.search(RegTimeSMs, txt):
        return TimeRangeType.SMs
    raise BadTimestamp("Bad timestamp: %s" % txt)


def parse_timestr(txt):
    """Converts VTT timestamp range to (start, end).

    Args:
        txt : str
            'hh:mm:ss.ms -> hh:mm:ss.ms' format timestamp range text
            (hh for hours, mm for minutes, ss for seconds, ms for millisec)

    Returns:
        Range (start, end) tuple of hh:mm:ss.ms format.
    """
    txt_fields = txt.strip().split()
    if len(txt_fields) != 3:
        raise BadTimestamp("Bad timestamp: %s" % txt)
    return txt_fields[0], txt_fields[2]


def parse_timestamp(txt):
    """Converts VTT timestamp hh:mm:ss.ms to milliseconds.

    Args:
        txt : str
            hh:mm:ss.ms format timestamp text
            (hh for hours, mm for minutes, ss for seconds, ms for millisec)

    Returns:
        Millisecond conversion from hh:mm:ss.ms timestamp representation.
    """
    ts_type = get_time_range_type(txt)
    if ts_type is TimeRangeType.HMSMs:
        return parse_time_range_hmsms(txt)
    elif ts_type is TimeRangeType.MSMs:
        return parse_time_range_msms(txt)
    elif ts_type is TimeRangeType.SMs:
        return parse_time_range_sms(txt)
    raise BadTimestamp("Bad timestamp: %s" % txt)


def parse_time_range_hmsms(txt):
    """Converts VTT timestamp hh:mm:ss.ms to milliseconds.

    Args:
        txt : str
            hh:mm:ss.ms format timestamp text
            (hh for hours, mm for minutes, ss for seconds, ms for millisec)

    Returns:
        Millisecond conversion from hh:mm:ss.ms timestamp representation.
    """
    h_m_s_ms = txt.strip().split(':')
    try:
        hr = int(h_m_s_ms[0])
        min = int(h_m_s_ms[1])
        s_ms = parse_time_range_sms(h_m_s_ms[2])
        return (hr * 36_00_000) + (min * 60_000) + s_ms
    except Exception as e:
        print(e)
        raise BadTimestamp("Bad hh:mm:ss.ms timestamp: %s" % txt)


def parse_time_range_msms(txt):
    """Converts VTT timestamp mm:ss.ms to milliseconds.

    Args:
        txt : str
            mm:ss.ms format timestamp text
            (mm for minutes, ss for seconds, ms for millisec)

    Returns:
        Millisecond conversion from mm:ss.ms timestamp representation.
    """
    m_s_ms = txt.strip().split(':')
    try:
        min = int(m_s_ms[0])
        s_ms = parse_time_range_sms(m_s_ms[1])
        return (min * 60_000) + s_ms
    except Exception as e:
        print(e)
        raise BadTimestamp("Bad mm:ss.ms timestamp: %s" % txt)


def parse_time_range_sms(txt):
    """Converts VTT timestamp ss.ms to milliseconds.

    Args:
        txt : str
            ss.ms format timestamp text (ss for seconds, ms for millisec)

    Returns:
        Millisecond conversion from ss.ms timestamp representation.
    """
    s_ms = txt.strip().split('.')
    try:
        sec = int(s_ms[0])
        msec = int(s_ms[1])
        return (sec * 1_000) + msec
    except Exception as e:
        print(e)
        raise BadTimestamp("Bad ss.ms timestamp: %s" % txt)
