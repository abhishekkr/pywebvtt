from pywebvtt import webvtt, errors
import pytest


def test_webvtt_init_failure():
    w = webvtt.WebVTT(vttfile='not-a-sample.vtt')
    assert w.vttfile == 'not-a-sample.vtt'
    with pytest.raises(errors.MissingFileError):
        w.ParseFile()


def test_webvtt_init_success():
    w = webvtt.WebVTT(vttfile='sample.vtt')
    assert w.vttfile == 'sample.vtt'
    w.ParseFile()
