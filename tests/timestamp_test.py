from pywebvtt import timestamp, errors
import pytest


def test_get_time_range_type():
    with pytest.raises(errors.BadTimestamp):
        timestamp.get_time_range_type('')
    with pytest.raises(errors.BadTimestamp):
        timestamp.get_time_range_type('00:00:00.00a')
    with pytest.raises(errors.BadTimestamp):
        timestamp.get_time_range_type('a0:00:00.000')
    with pytest.raises(errors.BadTimestamp):
        timestamp.get_time_range_type('0:00:00.000 1')
    ts_hmsm = timestamp.get_time_range_type('00:00:00.100')
    ts_msm = timestamp.get_time_range_type('00:00.100')
    ts_sm = timestamp.get_time_range_type('00.100')
    assert ts_hmsm == timestamp.TimeRangeType.HMSMs
    assert ts_msm == timestamp.TimeRangeType.MSMs
    assert ts_sm == timestamp.TimeRangeType.SMs


def test_parse_timestr():
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_timestr('')
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_timestr('00:00.000 - -> 00:00.100')
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_timestr('00:00.000-->00:00.100')
    ts_hmsm = timestamp.parse_timestr('00:00:00.000 -> 00:00:00.100')
    ts_msm = timestamp.parse_timestr('00:00.000 --> 00:00.100')
    assert ts_hmsm[0] == '00:00:00.000'
    assert ts_hmsm[1] == '00:00:00.100'
    assert ts_msm[0] == '00:00.000'
    assert ts_msm[1] == '00:00.100'


def test_parse_timestamp():
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_timestamp('')
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_timestamp('00:00:0a.00')
    ms_hmsm = timestamp.parse_timestamp('01:00:00.100')
    ms_msm = timestamp.parse_timestamp('00:00.100')
    assert ms_hmsm == 3600100
    assert ms_msm == 100


def test_parse_time_range_hmsms():
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_time_range_hmsms('')
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_time_range_hmsms('00:00.00')
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_time_range_hmsms('00.00')
    ms_hmsm = timestamp.parse_time_range_hmsms('01:10:01.100')
    assert ms_hmsm == 4201100


def test_parse_time_range_msms():
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_time_range_msms('')
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_time_range_msms('00:00:00.00')
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_time_range_msms('00.00')
    ms_msm = timestamp.parse_time_range_msms('10:01.100')
    assert ms_msm == 601100


def test_parse_time_range_sms():
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_time_range_sms('')
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_time_range_sms('00:00:00.00')
    with pytest.raises(errors.BadTimestamp):
        timestamp.parse_time_range_sms('00:00.00')
    ms_sm = timestamp.parse_time_range_sms('01.100')
    assert ms_sm == 1100
