import vlc
import time
import datetime
import os
import sys
import random


class WimHofBreather:
    testing_mode = True
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

    def lets_do_some_breathing(self):
        for round in range(1, self.breathing_sets + 1):

            self.play_breathing_audio(round)
            self.play_music_audio(round)
            self.play_15_second_breath_hold_audio()

    def play_breathing_audio(self, round):
        if round > 3:
            round = 'n'
        if self.testing_mode:
            wim_player = vlc.MediaPlayer(os.path.join(self.script_dir, 'audio/wim/breathing_testing.m4a'))
        else:
            wim_player = vlc.MediaPlayer(os.path.join(self.script_dir, f'audio/wim/breathing-{round}.mp3'))

        wim_player.play()
        time.sleep(1)  # Wait for audio to load and start playing

        while wim_player.is_playing():
            pass

    def play_music_audio(self, round):
        # Get a random song
        song_list = [f for f in os.listdir(os.path.join(self.script_dir, f"audio/song{round}")) if
                     f.endswith('mp3')]
        song = os.path.join(self.script_dir, f'audio/song{round}/' + random.choice(song_list))
        music_player = vlc.MediaPlayer(song)

        music_player.audio_set_volume(70)  # Wim doesn't talk very loud
        music_player.play()

        time_breathing = self.record_time_with_sentinel()
        self.breathing_times.append(time_breathing)

        # At this point, we want to stop playing the music audio and move on.
        if music_player.is_playing():
            music_player.stop()

    def play_15_second_breath_hold_audio(self):
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
