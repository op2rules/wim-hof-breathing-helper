from application.src.logmanager import LogManager
import datetime
import pytest

FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 5, 55, 12345)


@pytest.fixture
def patch_datetime_now(monkeypatch):
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime, 'datetime', mydatetime)


def test_ask_for_journal_entry(monkeypatch, capsys):
    logmanager = LogManager('test')

    # Use this to make the program think the user always confirms the journal entry, instead of having to
    # Dick around with the stdin a second time. This means we can't test the use case when a user wishes to
    # re-enter their journal entry, however.
    def return_true(_):
        return True

    monkeypatch.setattr(LogManager, "ask_user", return_true)

    # When Journal Entry is entered
    monkeypatch.setattr('builtins.input', lambda _: 'Journal Entry!')
    journal_entry = logmanager.ask_for_journal_entry()
    captured = capsys.readouterr()
    assert journal_entry == 'Journal Entry!'
    assert captured.out == 'Current Entry:  Journal Entry!\n'
    # When Journal Entry is not put in!
    monkeypatch.setattr('builtins.input', lambda _: '')
    journal_entry = logmanager.ask_for_journal_entry()
    captured = capsys.readouterr()
    assert journal_entry == 'No Entry'
    assert captured.out == 'Current Entry:  No Entry\n'


def test_ask_user(monkeypatch):
    logmanager = LogManager('test')
    # Check 'Y' Input
    monkeypatch.setattr('builtins.input', lambda _: 'Y')
    assert logmanager.ask_user() == True
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    assert logmanager.ask_user() == True
    # Check 'N' Input
    monkeypatch.setattr('builtins.input', lambda _: 'N')
    assert logmanager.ask_user() == False
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    assert logmanager.ask_user() == False
    # Check no input, which returns True
    monkeypatch.setattr('builtins.input', lambda _: '')
    assert logmanager.ask_user() == True


def test_save_entry(patch_datetime_now, tmpdir):
    file = tmpdir.mkdir('test').join('log.txt')
    logmanager = LogManager(file)
    breathing_times = [43, 180, 200, 205]
    journal_entry = 'Test Journal Entry'
    logmanager.save_entry(journal_entry, breathing_times)
    assert file.read() == "2020-12-25 17:05:55.012345\tTest Journal Entry\t43\t180\t200\t205\n"


def test_output_breathing_log(capsys, tmpdir):
    file = tmpdir.mkdir('test').join('log.txt')
    file.write("""
2021-03-01 00:42:57.935569\tEntry 1\t10\t20\t30\t40\t50
2021-03-02 00:43:08.413525\tEntry 2\t10\t20\t30\t40\t50
2021-03-03 00:43:10.890717\tEntry 3\t10\t20\t30\t40\t50
2021-03-04 00:43:37.294240\tEntry 4\t10\t20\t30\t40\t50
2021-03-05 00:43:37.985816\tNo Entry\t10\t20\t30\t40\t90
2021-03-06 00:43:38.985816\tLast Entry\t10\t20\t30\t40\t90
""")

    logmanager = LogManager(file)
    logmanager.output_breathing_log(4)
    captured = capsys.readouterr()

    assert captured.out == ("""
Mar 03 2021 -- 00:43\t\t0:10\t0:20\t0:30\t0:40\t0:50\t#: Entry 3
Mar 04 2021 -- 00:43\t\t0:10\t0:20\t0:30\t0:40\t0:50\t#: Entry 4
Mar 05 2021 -- 00:43\t\t0:10\t0:20\t0:30\t0:40\t1:30\t

Current Breathing Session_______________________________________
\x1b[92mMar 06 2021 -- 00:43\t\t0:10\t0:20\t0:30\t0:40\t1:30\t#: Last Entry\x1b[0m
""")


def test_convert_entry_to_pretty_output():
    logmanager = LogManager('test')

    # Regular Entry
    test_entry_string = '2021-03-05 00:43:37.985816\tEntry 5\t10\t20\t30\t40\t90'
    output = logmanager.convert_entry_to_pretty_output(test_entry_string)
    assert output == 'Mar 05 2021 -- 00:43\t\t0:10\t0:20\t0:30\t0:40\t1:30\t#: Entry 5'
    # No Entry
    test_entry_string = '2021-03-05 00:43:37.985816\tNo Entry\t10\t20\t30\t40\t90'
    output = logmanager.convert_entry_to_pretty_output(test_entry_string)
    assert output == 'Mar 05 2021 -- 00:43\t\t0:10\t0:20\t0:30\t0:40\t1:30\t'


def test_minutes_seconds_from_int():
    logmanager = LogManager('test')
    assert logmanager.minutes_seconds_from_int(200) == '3:20'
    assert logmanager.minutes_seconds_from_int(45) == '0:45'
    assert logmanager.minutes_seconds_from_int(1000) == '16:40'
    assert logmanager.minutes_seconds_from_int(9) == '0:09'
