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
    if TESTING_MODE:
        wim_player = vlc.MediaPlayer('wim-short.m4a')
    else:
        wim_player = vlc.MediaPlayer(f'breathing-{i}.mp3')
    wim_player.play()

    time.sleep(1)  # Wait for audio to load and start playing
    while wim_player.is_playing():
        pass

    breathing_music_player = vlc.MediaPlayer(f'./song{i}/' + random.choice(os.listdir(f"./song{i}")))
    breathing_music_player.play()

    time_breathing = record_time_with_sentinel()
    breathing_times.append(time_breathing)

    if breathing_music_player.is_playing():
        breathing_music_player.stop()

    # Play the 15 second breath hold
    # TODO: add debug
    b_player = vlc.MediaPlayer('15_second_hold.mp3')
    b_player.play()
    time.sleep(1)  # Wait for audio to load and start playing
    while (b_player.is_playing()):
        pass

print("Your breathing times were:")
for i in range(len(breathing_times)):
    if breathing_times[i] > 60:
        minutes = math.floor(breathing_times[i] / 60)
        seconds = breathing_times[i] - (minutes * 60)
        if len(str(seconds)) == 1:
            seconds = "0" + str(seconds)
        print(f"Set {i + 1}: {minutes}:{seconds}")
    else:
        print(f"Set {i + 1}: {breathing_times[i]} seconds")

today = str(datetime.date.today())
with open('breathing_log', 'a+') as log_file:
    log_file.write(today + ': ' + str(breathing_times) + '\n')
