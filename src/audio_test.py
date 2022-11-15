from pygame import mixer
import time


class AudioTest(object):

    def __init__(self, volume=1.0):
        self.base_audio_path = ("./audio/")
        self.songs = self.gather_songs()
        self.volume = volume

    # Make sure you populate the songs in the audio path
    def gather_songs(self):
        songs = [ "jingle.mp3", "rockin.mp3", "carol.mp3", "santa.mp3" ]
        return songs

    # Driver method
    def run(self):
        mixer.init()
        mixer.music.set_volume(self.volume)
        for song in self.songs:
            print(song)
            mixer.music.load("".join([self.base_audio_path, song]))
            mixer.music.play()
            time.sleep(5)
            mixer.music.stop()


def main():
    x = AudioTest()
    x.run()


if ((__name__) == ("__main__")):
    main()
