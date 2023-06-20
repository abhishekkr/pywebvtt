from enum import Enum
import re
from .errors import BadTimestamp

__all__ = ['TimeRangeType']


RegTimeHMSMs = r"\s*([0-9]+)\:([0-9]+)\:([0-9]+)\.([0-9]+)\s*"
RegTimeMSMs = r"\s*([0-9]+)\:([0-9]+)\.([0-9]+)\s*"
RegTimeSMs = r"\s*([0-9]+)\.([0-9]+)\s*"


class TimeRangeType(Enum):
    HMSMs = 1
    MSMs = 2
    SMs = 3


def get_time_range_type(str):
    if re.search(RegTimeHMSMs, str):
        return TimeRangeType.HMSMs
    elif re.search(RegTimeMSMs, str):
        return TimeRangeType.MSMs
    elif re.search(RegTimeSMs, str):
        return TimeRangeType.SMs
    raise BadTimestamp("Bad timestamp: %s" % str)


def parse_timestr(txt):
    txt_fields = txt.strip().split()
    if len(txt_fields) != 3:
        raise BadTimestamp("Bad timestamp: %s" % txt)
    return txt_fields[0], txt_fields[2]


def parse_timestamp(txt):
    ts_type = get_time_range_type(txt)
    if ts_type is TimeRangeType.HMSMs:
        return parse_time_range_hmsms(txt)
    elif ts_type is TimeRangeType.MSMs:
        return parse_time_range_msms(txt)
    elif ts_type is TimeRangeType.SMs:
        return parse_time_range_sms(txt)
    raise BadTimestamp("Bad timestamp: %s" % txt)


def parse_time_range_hmsms(txt):
    h_m_s_ms = txt.strip().split(':')
    if len(h_m_s_ms) != 3:
        raise BadTimestamp("Bad timestamp: %s" % txt)
    hr = int(h_m_s_ms[0])
    min = int(h_m_s_ms[1])
    s_ms = parse_time_range_sms(h_m_s_ms[2])
    return (hr * 36_00_000) + (min * 60_000) + s_ms


def parse_time_range_msms(txt):
    m_s_ms = txt.strip().split(':')
    if len(m_s_ms) != 2:
        raise BadTimestamp("Bad timestamp: %s" % txt)
    min = int(m_s_ms[0])
    s_ms = parse_time_range_sms(m_s_ms[1])
    return (min * 60_000) + s_ms


def parse_time_range_sms(txt):
    s_ms = txt.strip().split('.')
    if len(s_ms) != 2:
        raise BadTimestamp("Bad timestamp: %s" % txt)
    sec = int(s_ms[0])
    msec = int(s_ms[1])
    return (sec * 1_000) + msec
