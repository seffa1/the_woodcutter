import pygame as pg


class Audio_Manager:
    def __init__(self):
        self.sounds = {}
        self.music = {}
        self.load_audio()

    def load_audio(self):
        """ Saves the file locations of all sounds and music. """
        # Load Music
        self.music['Start_Screen'] = 'assets/music/Start_Screen.wav'
        self.music['Home_Music_1'] = 'assets/music/Home_Music_1.wav'
        self.music['Home_Music_2'] = 'assets/music/Home_Music_2.wav'
        self.music['Battle_Music_1'] = 'assets/music/Battle_Music_1.wav'
        self.music['Battle_Music_2'] = 'assets/music/Battle_Music_2.wav'
        self.music['Battle_Music_3'] = 'assets/music/Battle_Music_3.wav'

        # Load Sounds

    def play_sound(self, name, volume):
        """ Plays a stored sound file with a given volume from 0 to 1. """
        sound_effect = pg.mixer.Sound(self.sounds[name])
        sound_effect.set_volume(volume)
        sound_effect.play()
        # Only one music track can be playing at a time
        # Volume ranges from 0 to 1. Use decimal values

    def play_music(self, name, volume=0, num=-1):
        """ Plays a stored music file with a given volume and loop count. """
        pg.mixer.music.set_volume(volume)
        pg.mixer.music.load(self.music[name])
        # num determines how long the music plays, -1 means the music will loop indefinetly
        # -1 = loop, 0 = play once, 1 = plays twice, ...
        pg.mixer.music.play(num)

    def stop(self):
        """ Stops all sounds or music from playing. """
        pg.mixer.music.stop()
