from pywebvtt import scene, errors
import pytest


def test_parse():
    meta, discardObj = scene.parse('')
    assert meta == scene.Metadata.Discard
    assert discardObj is None

    meta, headerObj = scene.parse('WEBVTT')
    assert meta == scene.Metadata.Header
    assert headerObj is None

    meta, noteObj = scene.parse('NOTE alpha beta')
    assert meta == scene.Metadata.Note
    assert noteObj is None

    meta, timeObj = scene.parse('00:00.100 --> 00:10.000')
    assert meta == scene.Metadata.TimeRange
    assert timeObj.start_millisec == 100
    assert timeObj.end_millisec == 10_000

    meta, subObj = scene.parse('someone says something')
    assert meta == scene.Metadata.Subtext
    assert subObj is None


def test_is_header():
    assert scene.is_header('WEBVTT') is True
    assert scene.is_header('NOTE alpha beta') is False
    assert scene.is_header('00:00.100 --> 00:10.000') is False
    assert scene.is_header('someone says something') is False


def test_is_note():
    assert scene.is_note('WEBVTT') is False
    assert scene.is_note('NOTE alpha beta') is True
    assert scene.is_note('00:00.100 --> 00:10.000') is False
    assert scene.is_note('someone says something') is False


def test_is_timestamp():
    assert scene.is_timestamp('WEBVTT') is False
    assert scene.is_timestamp('NOTE alpha beta') is False
    assert scene.is_timestamp('00:00:00.100 --> 00:00:10.000') is True
    assert scene.is_timestamp('00:00.100 --> 00:10.000') is True
    assert scene.is_timestamp('00.100 --> 10.000') is True
    assert scene.is_timestamp('00.100 --> 00:05:10.000') is True
    assert scene.is_timestamp('someone says something') is False


def test_scene_init_failure():
    with pytest.raises(errors.BadTimestamp):
        scene.Scene(start='00:00:10.abc', end='00:00:10.000')


def test_scene_init_success():
    s = scene.Scene(start='00:00:10.000', end='00:00:10.500')
    assert s.start == '00:00:10.000'
    assert s.end == '00:00:10.500'
    assert s.start_millisec == 10_000
    assert s.end_millisec == 10_500


def test_scene_add_transcript():
    s = scene.Scene(start='00:00:10.000', end='00:00:10.500')
    s.add_transcript('alpha')
    assert s.transcript == ['alpha']
    s.add_transcript('beta')
    assert s.transcript == ['alpha', 'beta']
    s.add_transcript('theta')
    assert s.transcript == ['alpha', 'beta', 'theta']
