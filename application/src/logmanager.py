import math
import datetime
import os

class LogManager:
    script_dir = os.path.dirname(__file__)

    def __init__(self, log_file_path, absolute_path=False):
        if not absolute_path:
            self.log_file_path = os.path.join(self.script_dir, log_file_path)
        else:
            self.log_file_path = log_file_path

    def ask_for_journal_entry(self):
        # Ask the user to input a journal entry
        confirm = False
        while not confirm:
            journal_entry = input("Enter Journal entry\n")
            if len(journal_entry)==0:
                journal_entry = 'No Entry'
            print('Current Entry: ', journal_entry)
            if self.ask_user():
                confirm = True

        return(journal_entry)

    def ask_user(self):
        # This function asks for either yes or no.
        check = str(input("Is this correct? (Y/n): ")).lower().strip()
        try:
            if check == 'y':
                return True
            elif len(check) == 0:
                return True
            elif check == 'n':
                return False
            else:
                print('Invalid Input')
                return self.ask_user()
        except Exception as error:
            print("Please enter valid inputs")
            print(error)
            return self.ask_user()

    def save_entry(self, journal_entry, breathing_times):
        # Write an entire entry line to the log file

        # Convert the breathing times into a string separated with tabs
        times_str = list(map(str, breathing_times))
        times_for_tsv = '\t'.join(times_str)

        # Get the current date as a string.
        today = str(datetime.datetime.now())

        # Create the string to write to the logfile
        entry_string = today + '\t' + journal_entry + '\t' + times_for_tsv + '\n'

        # Write to the log file
        with open(self.log_file_path, 'a+') as log_file:
            log_file.write(entry_string)

    def output_breathing_log(self, number_of_lines):
        # Read the last n lines of the log, and pretty-print
        log_file = open(self.log_file_path, "r")
        lines = log_file.read().splitlines()
        last_n = lines[-number_of_lines:]

        pretty_last_n = list(map(self.convert_entry_to_pretty_output, last_n))
        pretty_last_n_current_time = pretty_last_n.pop()
        pretty_last_n_current_time = '\033[92m' + pretty_last_n_current_time + '\033[0m'

        print("")  # Empty line to space formatting down a bit

        for pretty_line in pretty_last_n:
            print(pretty_line)

        print("\nCurrent Breathing Session_______________________________________")
        print(pretty_last_n_current_time)

    def convert_entry_to_pretty_output(self, time_entry_line):
        # Convert to an array
        values = time_entry_line.split('\t')

        # Get the datetime. Pretty format it.
        entry_time = values[0]
        time_obj = datetime.datetime.strptime(entry_time, '%Y-%m-%d %H:%M:%S.%f')
        time_string = time_obj.strftime('%b %d %Y -- %H:%M')

        # Get the journal entry
        journal_entry = values[1]
        # Print nothing if
        if journal_entry == 'No Entry':
            journal_entry = ''
        else:
            journal_entry = '#: ' + journal_entry

        # For each of the breathing times, pretty format it into seconds and minutes
        breathing_seconds_from_log = list(map(int, values[2:]))
        breathing_pretty_from_log = map(self.minutes_seconds_from_int, breathing_seconds_from_log)
        return time_string + '\t\t' + '\t'.join(breathing_pretty_from_log) + '\t' + journal_entry

    def minutes_seconds_from_int(self, breathing_seconds):
        minutes = math.floor(breathing_seconds / 60)
        seconds = breathing_seconds - (minutes * 60)
        if seconds < 10:
            seconds = "0" + str(seconds)
        return str(minutes) + ':' + str(seconds)
