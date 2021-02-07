import vlc
import time
import math
import datetime
import os
import random


class WimHofBreather:
    testing_mode = True
    breathing_times = []

    def __init__(self):
        print("Alright, guys!")
        self.breathing_sets = int(input("How many breathing sets would you like to do?\n"))

    def get_breathing_times(self):
        return self.breathing_times

    def lets_do_some_breathing(self):
        for i in range(1, self.breathing_sets + 1):
            index = i
            if index > 3:
                index = 'n'
            if self.testing_mode:
                wim_player = vlc.MediaPlayer('audio/wim/breathing_testing.m4a')
            else:
                wim_player = vlc.MediaPlayer(f'./audio/wim/breathing-{index}.mp3')
            wim_player.play()

            time.sleep(1)  # Wait for audio to load and start playing
            while wim_player.is_playing():
                pass
            song_list = [f for f in os.listdir(f"./audio/song{index}") if f.endswith('mp3')]
            breathing_music_player = vlc.MediaPlayer(f'./audio/song{index}/' + random.choice(song_list))
            breathing_music_player.audio_set_volume(60)  # Wim doesn't talk very loud
            breathing_music_player.play()

            time_breathing = self.record_time_with_sentinel()
            self.breathing_times.append(time_breathing)

            if breathing_music_player.is_playing():
                breathing_music_player.stop()

            # Play the 15 second breath hold
            if self.testing_mode:
                b_player = vlc.MediaPlayer('./audio/wim/15_sec_testing.mp3')
            else:
                b_player = vlc.MediaPlayer('./audio/wim/15_second_hold.mp3')

            b_player.play()
            time.sleep(1)  # Wait for audio to load and start playing
            while (b_player.is_playing()):
                pass

    def record_time_with_sentinel(self):
        start_time = time.time()
        sentinel = "Breathing..."
        while sentinel == "Breathing...":
            sentinel = input("Press enter to continue")
        return round((time.time() - start_time))


class LogManager:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

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
        ## Read the last n lines of the log, and pretty-print
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
        time = values[0]
        time_obj = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
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


wim_hof_class = WimHofBreather()
wim_hof_class.lets_do_some_breathing()

log_manager = LogManager('breathing_log.tsv')
log_manager.save_breathing_time_to_today(wim_hof_class.get_breathing_times())
log_manager.output_breathing_log(5)

print("\nWim would be proud :)")
