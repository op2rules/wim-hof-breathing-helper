import vlc
import time
import math
import datetime
import os
import random

TESTING_MODE = False


def record_time_with_sentinel():
    start_time = time.time()
    sentinel = "Breathing..."
    while sentinel == "Breathing...":
        sentinel = input("Press enter to continue")
    return round((time.time() - start_time))


breathing_sets = int(input("How many breathing sets would you like to do?\n"))
breathing_times = []

for i in range(1, breathing_sets + 1):
    index = i
    if index > 3:
        index = 'n'
    if TESTING_MODE:
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

    time_breathing = record_time_with_sentinel()
    breathing_times.append(time_breathing)

    if breathing_music_player.is_playing():
        breathing_music_player.stop()

    # Play the 15 second breath hold
    if TESTING_MODE:
        b_player = vlc.MediaPlayer('./audio/wim/15_sec_testing.mp3')
    else:
        b_player = vlc.MediaPlayer('./audio/wim/15_second_hold.mp3')

    b_player.play()
    time.sleep(1)  # Wait for audio to load and start playing
    while (b_player.is_playing()):
        pass

## Write the times to the log file.
# Convert the breathing times to strings 
times_str = list(map(str, breathing_times))
string_for_tsv = '\t'.join(times_str)
# Get the current date as a string.
today = str(datetime.datetime.now())
log_file_path = 'breathing_log.tsv'
# Add all to the log
with open(log_file_path, 'a+') as log_file:
    log_file.write(today + '\t' + string_for_tsv + '\n')

## Read the last n lines of the log, and pretty-print
log_file = open(log_file_path, "r")
lines = log_file.reads().splitlines()
n = 5
last_n = lines[-n:]

# For each of the retreived lines.
for line in last_n: 

    # Convert to an array
    values = line.split('\t')
    # Get the time. Pretty format it.
    time = values[0]
    time_obj = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    print(time_obj.strftime('%b %d %Y -- %H:%M'))

    # For each of the times, pretty format it into seconds and minutes
    breathing_seconds = list(map(int, values[1:]))
    breathing_pretty = []
    for i in range(len(breathing_seconds)):

        minutes = math.floor(breathing_seconds[i] / 60)
        seconds = breathing_seconds[i] - (minutes * 60)
        if seconds < 10:
            seconds = "0" + str(seconds)
        breathing_pretty.append(str(minutes) + ':' + str(seconds))


