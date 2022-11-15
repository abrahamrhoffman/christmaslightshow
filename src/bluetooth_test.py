from bluetooth.ble import DiscoveryService
from pygame import mixer
import time


class BluetoothTest(object):

    def __init__(self, volume=1.0):
        self.show_connected_ble_devices()
        mixer.init()  # Unfortunately, class variables are ugly with mixer
        self.base_audio_path = ("./audio/")
        self.songs = self.gather_songs()
        mixer.music.set_volume(volume)

    def gather_songs(self):
        songs = [ "jingle.mp3", "rockin.mp3", "carol.mp3", "santa.mp3" ]
        return songs

    # Expecting only Bluetooth Low Energy Devices to be connected: YMMV
    def show_connected_ble_devices(self):
        service = DiscoveryService()
        devices = service.discover(2)
        for device in devices.items():
            print(device)

    # Driver method
    def run(self):
        for song in self.songs:
            mixer.music.load("".join([self.base_audio_path, song]))
            mixer.music.play()
            time.sleep(5)
            mixer.music.stop()


def main():
    x = BluetoothTest()
    x.run()


if ((__name__) == ("__main__")):
    main()
