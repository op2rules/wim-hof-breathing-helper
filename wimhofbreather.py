import vlc
import time
import datetime
import os
import sys
import random


class WimHofBreather:
    testing_mode = False
    breathing_times = []
    random.seed(datetime.datetime.now())

    def __init__(self):
        print("Alright, guys!")
        self.breathing_sets = int(input("How many breathing sets would you like to do?\n"))
        self.script_dir = os.path.dirname(__file__)
        if len(sys.argv) > 1 and sys.argv[1] == "debug":
            self.testing_mode = True

    def get_breathing_times(self):
        return self.breathing_times

    def get_breathing_player(self, index):
        if index > 3:
            index = 'n'
        if self.testing_mode:
            wim_player = vlc.MediaPlayer(os.path.join(self.script_dir, 'audio/wim/breathing_testing.m4a'))
        else:
            wim_player = vlc.MediaPlayer(os.path.join(self.script_dir, f'audio/wim/breathing-{index}.mp3'))

        return(wim_player)

    def get_music_player(self, index):

        # Get a random song
        song_list = [f for f in os.listdir(os.path.join(self.script_dir, f"audio/song{index}")) if
                     f.endswith('mp3')]
        song = os.path.join(self.script_dir, f'audio/song{index}/' + random.choice(song_list))
        music_player = vlc.MediaPlayer(song)

        music_player.audio_set_volume(70)  # Wim doesn't talk very loud
        return(music_player)


    def lets_do_some_breathing(self):

        for index in range(1, self.breathing_sets + 1):

            wim_player = self.get_breathing_player(index)
            wim_player.play()
            time.sleep(1)  # Wait for audio to load and start playing
            while wim_player.is_playing():
                pass

            music_player = self.get_music_player(index)
            music_player.play()

            time_breathing = self.record_time_with_sentinel()
            self.breathing_times.append(time_breathing)

            if music_player.is_playing():
                music_player.stop()

            # Play the 15 second breath hold
            if self.testing_mode:
                b_player = vlc.MediaPlayer(os.path.join(self.script_dir, 'audio/wim/15_sec_testing.mp3'))
            else:
                b_player = vlc.MediaPlayer(os.path.join(self.script_dir, 'audio/wim/15_second_hold.mp3'))

            b_player.play()
            time.sleep(1)  # Wait for audio to load and start playing
            while b_player.is_playing():
                pass

    def record_time_with_sentinel(self):
        start_time = time.time()
        sentinel = "Breathing..."
        while sentinel == "Breathing...":
            sentinel = input("Press enter to continue")
        return round((time.time() - start_time))
