import math
import datetime
import os

class LogManager:
    script_dir = os.path.dirname(__file__)

    def __init__(self, log_file_path):
        self.log_file_path = os.path.join(self.script_dir, log_file_path)

    def save_breathing_time_to_today(self, breathing_time_string):
        formatted_day_string = self.convert_breathing_times_to_strings(breathing_time_string)
        with open(self.log_file_path, 'a+') as log_file:
            log_file.write(formatted_day_string)

    def convert_breathing_times_to_strings(self, breathing_times):
        times_str = list(map(str, breathing_times))
        string_for_tsv = '\t'.join(times_str)
        # Get the current date as a string.
        today = str(datetime.datetime.now())
        return today + '\t' + string_for_tsv + '\n'

    def output_breathing_log(self, number_of_lines):
        # Read the last n lines of the log, and pretty-print
        log_file = open(self.log_file_path, "r")
        lines = log_file.read().splitlines()
        last_n = lines[-number_of_lines:]

        pretty_last_n = list(map(self.convert_time_entry_to_pretty_output, last_n))
        pretty_last_n_current_time = pretty_last_n.pop()
        pretty_last_n_current_time = '\033[92m' + pretty_last_n_current_time + '\033[0m'

        print("")  # Empty line to space formatting down a bit

        for pretty_line in pretty_last_n:
            print(pretty_line)

        print("\nCurrent Breathing Session_______________________________________")
        print(pretty_last_n_current_time)

    def convert_time_entry_to_pretty_output(self, time_entry_line):
        # Convert to an array
        values = time_entry_line.split('\t')
        # Get the time. Pretty format it.
        entry_time = values[0]
        time_obj = datetime.datetime.strptime(entry_time, '%Y-%m-%d %H:%M:%S.%f')
        time_string = time_obj.strftime('%b %d %Y -- %H:%M')

        # For each of the times, pretty format it into seconds and minutes
        breathing_seconds_from_log = list(map(int, values[1:]))
        breathing_pretty_from_log = map(self.minutes_seconds_from_int, breathing_seconds_from_log)
        return time_string + '\t\t' + '\t'.join(breathing_pretty_from_log)

    def minutes_seconds_from_int(self, breathing_seconds):
        minutes = math.floor(breathing_seconds / 60)
        seconds = breathing_seconds - (minutes * 60)
        if seconds < 10:
            seconds = "0" + str(seconds)
        return str(minutes) + ':' + str(seconds)
