#!/usr/bin/python3
from pygame import mixer
import RPi.GPIO as GPIO
import random
import glob
import time


class LightShow(object):

    def __init__(self, volume=1.0, gpio_speed=0.166):
        self.base_audio_path = ("./audio/")
        self.base_sequence_path = ("./sequences/")
        self.songs = self.gather_songs()
        self.sequences = self.gather_sequences()
        self.volume = volume
        GPIO.setwarnings(False)   # Disable GPIO in use warnings
        GPIO.setmode(GPIO.BOARD)  # Set the GPIO mode to BOARD using pin integer
        self.channels = self.configure_channels()
        self.speed=gpio_speed

    def gather_songs(self):
        songs = glob.glob("".join([self.base_audio_path, "*"]))
        return sorted(songs)

    def gather_sequences(self):
        sequences = glob.glob("".join([self.base_sequence_path, "*"]))
        return sorted(sequences)

    # Channels are Solid State Relay Channels
    # Actual numbers are the RPi 4 BOARD pin integers
    def configure_channels(self):
        channel_0 = 11
        channel_1 = 12
        channel_2 = 13
        channel_3 = 15
        channel_4 = 16
        channel_5 = 18
        # channel_6 = 22
        # channel_7 = 24
        channels = [
            channel_0, channel_1, channel_2, channel_3,
            channel_4, channel_5 #, channel_6, channel_7,
        ]
        return channels

    # Turn off all GPIOs
    def all_off(self):
        try:
            for channel in self.channels:
                GPIO.output(channel, False)
        except RuntimeError:
            # Maybe all the GPIOs are already off
            pass

    # Cycle GPIOs forward
    def forward(self):
        for channel in self.channels:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
            time.sleep(self.speed)
            GPIO.output(channel, False)

    # Cycle GPIOs reverse
    def reverse(self):
        for channel in self.channels[::-1]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
            time.sleep(self.speed)
            GPIO.output(channel, False)

    # Cycle GPIOs randomly (using a LCG)
    def random_selection(self):
        for channel in [random.choice(self.channels) for _ in range(0, 16)]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
            time.sleep(self.speed)
            GPIO.output(channel, False)

    # Cycle GPIOs from the outside channels to the inside channels
    def outside_in(self):
        left_side = self.channels[0:4]
        right_side = self.channels[4:8][::-1]
        for lc, rc in zip(left_side, right_side):
            GPIO.setup(lc, GPIO.OUT)
            GPIO.output(lc, True)
            GPIO.setup(rc, GPIO.OUT)
            GPIO.output(rc, True)
            time.sleep(self.speed)
            GPIO.output(lc, False)
            GPIO.output(rc, False)

    # Cycle GPIOs from the inside channels to the outside channels
    def inside_out(self):
        left_side = self.channels[0:4][::-1]
        right_side = self.channels[4:8]
        for lc, rc in zip(left_side, right_side):
            GPIO.setup(lc, GPIO.OUT)
            GPIO.output(lc, True)
            GPIO.setup(rc, GPIO.OUT)
            GPIO.output(rc, True)
            time.sleep(self.speed)
            GPIO.output(lc, False)
            GPIO.output(rc, False)

    def split_channels_one(self):
        split_channels = [ self.channels[0], self.channels[2], self.channels[4], self.channels[6] ]
        for channel in split_channels:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        time.sleep(1)
        for channel in split_channels:
            GPIO.output(channel, False)

    def split_channels_two(self):
        split_channels = [ self.channels[1], self.channels[3], self.channels[5], self.channels[7] ]
        for channel in split_channels:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        time.sleep(1)
        for channel in split_channels:
            GPIO.output(channel, False)

    def all_on(self):
        for channel in self.channels:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        time.sleep(1)
        for channel in self.channels:
            GPIO.output(channel, False)

    def run(self):
        for song, sequence in zip(self.songs, self.sequences):
            print(song, sequence)

            with open(sequence, "r") as f:
                sequence_data = f.readlines()
                for i in range(len(sequence_data)):
                    sequence_data[i] = sequence_data[i].rstrip()

            # Play the song #
            mixer.init()
            mixer.music.set_volume(self.volume)
            mixer.music.load(song)
            mixer.music.play()

            # Set the start time and current time
            start_time = int(round(time.time() * 1000))
            current_time = (int(round(time.time() * 1000)) - start_time)

            # Instead of blindly blocking on a while True, step through each timestep.
            # When the timestep in the sequence matches, trigger the GPIO actions in the sequence file
            for ix, step in enumerate(sequence_data[1:]):
                print(step)
                while (int(step.split(",")[0]) >= current_time):
                    current_time = (int(round(time.time() * 1000)) - start_time)
                    time.sleep(0.1)
                    if current_time % 500 == 0:
                        print(step.split(",")[0], current_time)

                # Once the timestep is reached, trigger the action in the sequence file
                action = step.split(",")[1]
                print(action)
                if action == "ALL_OFF":
                    self.all_off()
                elif action == "ALL_ON":
                    self.all_on()
                elif action == "FORWARD":
                    self.forward()
                elif action == "REVERSE":
                    self.reverse()
                elif action == "RANDOM":
                    self.random_selection()
                elif action == "OUTSIDE_IN":
                    self.outside_in()
                elif action == "INSIDE_OUT":
                    self.inside_out()
                elif action == "SPLIT_CHANNELS_ONE":
                    self.split_channels_one()
                elif action == "SPLIT_CHANNELS_TWO":
                    self.split_channels_two()
                elif action == "END":
                    # Move on to the next song-sequence pair or exit 0
                    break


def main():
    x = LightShow()
    x.run()


if ((__name__) == ("__main__")):
    main()