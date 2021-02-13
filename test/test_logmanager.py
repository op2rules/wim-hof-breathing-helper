import datetime
import pytest
from logmanager import LogManager

FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 5, 55, 12345)


@pytest.fixture
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime, 'datetime', mydatetime)


def test_convert_breathing_times_to_strings(patch_datetime_now):
    logmanager = LogManager('test')
    breathing_times = [43, 180, 200, 205]
    converted_string = logmanager.convert_breathing_times_to_strings(breathing_times)

    assert converted_string == '2020-12-25 17:05:55.012345\t43\t180\t200\t205\n'


def test_output_breathing_log(capsys):
    logmanager = LogManager('test/test_breathing_log.tsv')
    logmanager.output_breathing_log(5)
    captured = capsys.readouterr()

    assert captured.out == ("""
Feb 06 2021 -- 22:12		0:01
Feb 06 2021 -- 22:33		0:03	0:01
Feb 06 2021 -- 22:34		0:05
Feb 06 2021 -- 22:36		0:03

Current Breathing Session_______________________________________
\x1b[92mFeb 07 2021 -- 15:26		0:05\x1b[0m
""")


def test_convert_time_entry_to_pretty_output():
    logmanager = LogManager('xxx')
    string = logmanager.convert_time_entry_to_pretty_output('2015-12-25 17:05:55.31337\t43\t180\t200\t205')

    assert string == "Dec 25 2015 -- 17:05\t\t0:43\t3:00\t3:20\t3:25"


def test_minutes_seconds_from_int():
    logmanager = LogManager('xxx')
    assert logmanager.minutes_seconds_from_int(200) == '3:20'
    assert logmanager.minutes_seconds_from_int(45) == '0:45'
    assert logmanager.minutes_seconds_from_int(1000) == '16:40'
    assert logmanager.minutes_seconds_from_int(9) == '0:09'


def test_save_breathing_time_to_today(patch_datetime_now, tmpdir):
    file = tmpdir.join('output.txt')
    logmanager = LogManager(file)
    logmanager.save_breathing_time_to_today([200, 45, 1000, 9])
    assert file.read() == "2020-12-25 17:05:55.012345\t200\t45\t1000\t9\n"
