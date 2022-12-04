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
        channels = [ channel_0, channel_1, channel_2, channel_3, channel_4, channel_5 ]
        return channels

    # Pair channel: 0,3
    def pair_one(self, custom_speed=False):
        for channel in [self.channels[0], self.channels[3]]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in [self.channels[0], self.channels[3]]:
            GPIO.output(channel, False)

    # Pair channel: 1,4
    def pair_two(self, custom_speed=False):
        for channel in [self.channels[1], self.channels[4]]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in [self.channels[1], self.channels[4]]:
            GPIO.output(channel, False)

    # Pair channel: 2,5
    def pair_three(self, custom_speed=False):
        for channel in [self.channels[2], self.channels[5]]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in [self.channels[2], self.channels[5]]:
            GPIO.output(channel, False)

    # Pair channel: 0,5
    def diagonal_one(self, custom_speed=False):
        for channel in [self.channels[0], self.channels[5]]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in [self.channels[0], self.channels[5]]:
            GPIO.output(channel, False)

    # Pair channel: 2,3
    def diagonal_two(self, custom_speed=False):
        for channel in [self.channels[2], self.channels[3]]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in [self.channels[2], self.channels[3]]:
            GPIO.output(channel, False)

    # Pair channel: 0,4
    def down_right_one(self, custom_speed=False):
        for channel in [self.channels[0], self.channels[4]]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in [self.channels[0], self.channels[4]]:
            GPIO.output(channel, False)

    # Pair channel: 1,5
    def down_right_two(self, custom_speed=False):
        for channel in [self.channels[1], self.channels[5]]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in [self.channels[1], self.channels[5]]:
            GPIO.output(channel, False)

    # Pair channel: 1,3
    def down_left_one(self, custom_speed=False):
        for channel in [self.channels[1], self.channels[3]]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in [self.channels[1], self.channels[3]]:
            GPIO.output(channel, False)

    # Pair channel: 2,4
    def down_left_two(self, custom_speed=False):
        for channel in [self.channels[2], self.channels[4]]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in [self.channels[2], self.channels[4]]:
            GPIO.output(channel, False)

    def all_on(self, custom_speed=False):
        for channel in self.channels:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in self.channels:
            GPIO.output(channel, False)

    # Turn off all GPIOs
    def all_off(self):
        try:
            for channel in self.channels:
                GPIO.output(channel, False)
        except RuntimeError:
            # Maybe all (or one) of the GPIOs are already off
            pass

    # Cycle GPIOs forward
    def forward(self, custom_speed=False):
        channels = [
            self.channels[0], self.channels[1], self.channels[2],
            self.channels[5], self.channels[4], self.channels[3]
        ]
        for channel in channels:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
            if custom_speed:
                time.sleep(float(int(custom_speed) / 1000))
            else:
                time.sleep(self.speed)
            GPIO.output(channel, False)

    # Cycle GPIOs reverse
    def reverse(self, custom_speed=False):
        channels = [
            self.channels[3], self.channels[4], self.channels[5],
            self.channels[2], self.channels[1], self.channels[0]
        ]
        for channel in channels:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
            if custom_speed:
                time.sleep(float(int(custom_speed) / 1000))
            else:
                time.sleep(self.speed)
            GPIO.output(channel, False)

    # Cycle GPIOs randomly (using a LCG)
    def random_selection(self, custom_speed=False):
        for channel in [random.choice(self.channels) for _ in range(0, 12)]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
            if custom_speed:
                time.sleep(float(int(custom_speed) / 1000))
            else:
                time.sleep(self.speed)
            GPIO.output(channel, False)

    # Cycle GPIOs from the outside channels to the inside channels
    def outside_in(self, custom_speed=False):
        for channel in [self.channels[0], self.channels[2], self.channels[3], self.channels[5]]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in [self.channels[0], self.channels[2], self.channels[3], self.channels[5]]:
            GPIO.output(channel, False)

        for channel in [self.channels[1], self.channels[4]]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in [self.channels[1], self.channels[4]]:
            GPIO.output(channel, False)

    # Cycle GPIOs from the inside channels to the outside channels
    def inside_out(self, custom_speed=False):
        for channel in [self.channels[1], self.channels[4]]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in [self.channels[1], self.channels[4]]:
            GPIO.output(channel, False)

        for channel in [self.channels[0], self.channels[2], self.channels[3], self.channels[5]]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in [self.channels[0], self.channels[2], self.channels[3], self.channels[5]]:
            GPIO.output(channel, False)

    def split_channels_one(self, custom_speed=False):
        split_channels = [ self.channels[0], self.channels[4], self.channels[2] ]
        for channel in split_channels:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in split_channels:
            GPIO.output(channel, False)

    def split_channels_two(self, custom_speed=False):
        split_channels = [ self.channels[1], self.channels[3], self.channels[5] ]
        for channel in split_channels:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
        if custom_speed:
            time.sleep(float(int(custom_speed) / 1000))
        else:
            time.sleep(self.speed)
        for channel in split_channels:
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
            # When the timestep in the sequence (approximately) matches, trigger the GPIO actions in the sequence file
            # In practice, this approximate timing has always been close enough to be accurate.
            for step in sequence_data[1:]:
                while (int(step.split(",")[0]) >= current_time):
                    current_time = (int(round(time.time() * 1000)) - start_time)
                    time.sleep(0.1)  # Can decrease for higher accuracy - causes more CPU load

                # Once the timestep is reached, trigger the action in the sequence file
                timestep = step.split(",")[0]
                action = step.split(",")[1]
                duration = step.split(",")[2]
                print(f"{timestep} :: {action} {duration}")
                if action == "ALL_ON":
                    if duration != "":
                        self.all_on(custom_speed=duration)
                    else:
                        self.all_on()
                elif action == "ALL_OFF":
                    if duration != "":
                        self.all_off(custom_speed=duration)
                    else:
                        self.all_off()
                elif action == "PAIR_ONE":
                    if duration != "":
                        self.pair_one(custom_speed=duration)
                    else:
                        self.pair_one()
                elif action == "PAIR_TWO":
                    if duration != "":
                        self.pair_two(custom_speed=duration)
                    else:
                        self.pair_two()
                elif action == "PAIR_THREE":
                    if duration != "":
                        self.pair_three(custom_speed=duration)
                    else:
                        self.pair_three()
                elif action == "DIAGONAL_ONE":
                    if duration != "":
                        self.diagonal_one(custom_speed=duration)
                    else:
                        self.diagonal_one()
                elif action == "DIAGONAL_TWO":
                    if duration != "":
                        self.diagonal_two(custom_speed=duration)
                    else:
                        self.diagonal_two()
                elif action == "DOWN_RIGHT_ONE":
                    if duration != "":
                        self.down_right_one(custom_speed=duration)
                    else:
                        self.down_right_one()
                elif action == "DOWN_RIGHT_TWO":
                    if duration != "":
                        self.down_right_two(custom_speed=duration)
                    else:
                        self.down_right_two()
                elif action == "DOWN_LEFT_ONE":
                    if duration != "":
                        self.down_left_one(custom_speed=duration)
                    else:
                        self.down_left_one()
                elif action == "DOWN_LEFT_TWO":
                    if duration != "":
                        self.down_left_two(custom_speed=duration)
                    else:
                        self.down_left_two()
                elif action == "FORWARD":
                    if duration != "":
                        self.forward(custom_speed=duration)
                    else:
                        self.forward()
                elif action == "REVERSE":
                    if duration != "":
                        self.reverse(custom_speed=duration)
                    else:
                        self.reverse()
                elif action == "RANDOM":
                    if duration != "":
                        self.random_selection(custom_speed=duration)
                    else:
                        self.random_selection()
                elif action == "OUTSIDE_IN":
                    if duration != "":
                        self.outside_in(custom_speed=duration)
                    else:
                        self.outside_in()
                elif action == "INSIDE_OUT":
                    if duration != "":
                        self.inside_out(custom_speed=duration)
                    else:
                        self.inside_out()
                elif action == "SPLIT_CHANNELS_ONE":
                    if duration != "":
                        self.split_channels_one(custom_speed=duration)
                    else:
                        self.split_channels_one()
                elif action == "SPLIT_CHANNELS_TWO":
                    if duration != "":
                        self.split_channels_two(custom_speed=duration)
                    else:
                        self.split_channels_two()
                elif action == "END":
                    # Move on to the next song-sequence pair or exit 0
                    break


def main():
    x = LightShow()
    x.run()


if ((__name__) == ("__main__")):
    main()