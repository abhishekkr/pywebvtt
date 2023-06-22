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
    assert scene.is_timestamp('') is False
    assert scene.is_timestamp('00:00:00.000') is False
    assert scene.is_timestamp('00:00:00.000 -> a0:00:00.000') is False
    assert scene.is_timestamp('00:00:00.000 -> 0:00:00.000 1') is False
    assert scene.is_timestamp('00:00.000 > 00:00.100') is False


def test_millisec_to_timestamp():
    with pytest.raises(errors.BadTimestamp):
        scene.millisec_to_timestamp('')
    with pytest.raises(errors.BadTimestamp):
        scene.millisec_to_timestamp('a:00:00.000')
    assert scene.millisec_to_timestamp(10) == '00:00.010'
    assert scene.millisec_to_timestamp(1010) == '00:01.010'
    assert scene.millisec_to_timestamp(101010) == '01:41.010'
    assert scene.millisec_to_timestamp(10101010) == '02:48:21.010'


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


def test_scene_sub_txt():
    s = scene.Scene(start='00:00:10.000', end='00:00:10.500')
    s.transcript = ['lorem', 'ipsum']
    assert s.sub_txt() == 'lorem\nipsum'
    s.transcript = ['- lorem', '- ipsum']
    assert s.sub_txt() == 'lorem\nipsum'

def test_scene_split_transcript():
    s = scene.Scene(start='00:00:10.000', end='00:00:10.500')
    s.transcript = ['lorem ipsum', 'is a random mumble wrap']
    split_text = s.split_transcript(10)
    assert len(split_text) == 5
    assert split_text[0] == 'lorem'
    assert split_text[1] == 'ipsum is a'
    assert split_text[2] == 'random'
    assert split_text[3] == 'mumble'
    assert split_text[4] == 'wrap'
    split_text_2 = s.split_transcript(15)
    assert len(split_text_2) == 3
    assert split_text_2[0] == 'lorem ipsum is'
    assert split_text_2[1] == 'a random mumble'
    assert split_text_2[2] == 'wrap'

def test_scene_duration_ms():
    s = scene.Scene(start='00:00:10.000', end='00:00:10.500')
    assert s.duration_ms() == 500

def test_scene_line_count():
    s = scene.Scene(start='00:00:10.000', end='00:00:10.500')
    assert s.line_count() == 0
    s.transcript = ['lorem', 'ipsum']
    assert s.line_count() == 2

def test_scene_char_counts():
    s = scene.Scene(start='00:00:10.000', end='00:00:10.500')
    assert s.char_counts() == []
    s.transcript = ['lorem', 'ipsum']
    assert s.char_counts() == [5, 5]

def test_scene_char_total():
    s = scene.Scene(start='00:00:10.000', end='00:00:10.500')
    assert s.char_total() == 0
    s.transcript = ['lorem', 'ipsum']
    assert s.char_total() == 10
