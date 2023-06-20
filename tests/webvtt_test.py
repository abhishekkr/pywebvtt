from pywebvtt import webvtt, errors
import pytest


def test_webvtt_init_failure():
    w = webvtt.WebVTT(vttfile='not-a-sample.vtt')
    assert w.vttfile == 'not-a-sample.vtt'
    with pytest.raises(errors.MissingFileError):
        w.parse_file()


def test_webvtt_init_success():
    w = webvtt.WebVTT(vttfile='sample.vtt')
    assert w.vttfile == 'sample.vtt'
    w.parse_file()


def test_webvtt_parse_file():
    w = webvtt.WebVTT(vttfile='sample.vtt')
    s = w.parse_file()
    # first scene
    assert s[0].start_millisec == 1_000
    assert s[0].end_millisec == 4_000
    assert len(s[0].transcript) == 1
    assert s[0].transcript == ['This is subtitle at 1sec to 4sec.']
    # second scene
    assert s[1].start_millisec == 5_000
    assert s[1].end_millisec == 9_000
    assert len(s[1].transcript) == 2
    # third scene
    assert s[2].start_millisec == 10_000
    assert s[2].end_millisec == 14_000
    assert len(s[2].transcript) == 1
