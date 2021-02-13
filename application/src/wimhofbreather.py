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

    def lets_do_some_breathing(self):
        for round in range(1, self.breathing_sets + 1):

            if round > 3:
                round = 'n'

            self.play_breathing_audio(round)

            if round<=3:
                list_player = self.get_vlc_MediaListPLayer(round)
                list_player = self.play_music_audio(list_player)
            else:
                list_player = self.play_music_audio(list_player)

            self.play_15_second_breath_hold_audio()

    def play_breathing_audio(self, round):
        if self.testing_mode:
            wim_player = vlc.MediaPlayer(os.path.join(self.script_dir, 'audio/wim/breathing_testing.m4a'))
        else:
            wim_player = vlc.MediaPlayer(os.path.join(self.script_dir, f'audio/wim/breathing-{round}.mp3'))

        wim_player.play()
        time.sleep(1)  # Wait for audio to load and start playing

        while wim_player.is_playing():
            pass

    def play_music_audio(self, list_player):
        list_player.next()
        # Get the vlc player so we can set the volume
        music_player = list_player.get_media_player()
        music_player.audio_set_volume(70)
        # Record the time and prompt for input
        time_breathing = self.record_time_with_sentinel()
        self.breathing_times.append(time_breathing)
        # At this point, we want to stop playing the music audio and move on.
        if list_player.is_playing():
            list_player.pause()
        return(list_player)

    def get_song_file_paths(self, round):
        song_dir = os.path.join(self.script_dir, f"audio/song{round}")
        song_list = []
        for dirpath, _, files in os.walk(song_dir):
            for f in files:
                file_path = os.path.join(dirpath, f)
                song_list.append(file_path)
        return(song_list)

    def get_vlc_MediaListPLayer(self, round):
        # Get song list
        song_list = self.get_song_file_paths(round)
        # Shuffle!
        random.shuffle(song_list)
        # Create the music player list
        Instance = vlc.Instance()
        Media_list = Instance.media_list_new(song_list)
        list_player = Instance.media_list_player_new()
        list_player.set_media_list(Media_list)
        return(list_player)

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
