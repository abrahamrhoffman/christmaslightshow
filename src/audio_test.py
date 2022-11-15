#!/usr/bin/python3
from pygame import mixer
import glob
import time


class AudioTest(object):

    def __init__(self, volume=1.0):
        self.base_audio_path = ("./audio/")
        self.songs = self.gather_songs()
        self.volume = volume

    # Make sure you populate the songs in the audio path
    def gather_songs(self):
        songs = glob.glob("".join([self.base_audio_path, "*"]))
        return songs

    # Driver method
    def run(self):
        mixer.init()
        mixer.music.set_volume(self.volume)
        for song in self.songs:
            print(song.split("/")[-1])
            mixer.music.load(song)
            mixer.music.play()
            time.sleep(5)
            mixer.music.stop()


def main():
    x = AudioTest()
    x.run()


if ((__name__) == ("__main__")):
    main()
