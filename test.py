import vlc

# TODO: Shuffle all the songs of the folder, and add them to a vlc instance as in the below code. For song-n interations,
# load the whole playlist, but keep the instance open between rounds, and play the next song in the playlist on the next round.

playlist = ['audio/wim/breathing_testing.m4a',
            'audio/wim/15_sec_testing.mp3',
            'audio/wim/breathing_testing.m4a',
            'audio/wim/15_sec_testing.mp3']

Instance = vlc.Instance()
Media_list = Instance.media_list_new(playlist)
list_player = Instance.media_list_player_new()
list_player.set_media_list(Media_list)
list_player.play()

list_player.is_playing()

music_player = vlc.MediaListPlayer(playlist)

music_player = vlc.MediaPlayer('audio/wim/breathing_testing.m4a')

type(music_player)
type(player)

music_player.audio_set_volume(70)  # Wim doesn't talk very loud
music_player.play()

if music_player.is_playing():

time_breathing = self.record_time_with_sentinel()
self.breathing_times.append(time_breathing)

# At this point, we want to stop playing the music audio and move on.
if music_player.is_playing():
    music_player.stop()

