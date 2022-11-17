#!/usr/bin/python3
import RPi.GPIO as GPIO
import random
import time


class GPIOTest(object):

    def __init__(self, speed=0.25):
        GPIO.setwarnings(False)   # Disable GPIO in use warnings
        GPIO.setmode(GPIO.BOARD)  # Set the GPIO mode to BOARD using pin integer
        self.channels = self.configure_channels()
        self.speed=speed

    # Channels are Solid State Relay Channels
    # Actual numbers are the RPi 4 BOARD pin integers
    def configure_channels(self):
        channel_0 = 11
        channel_1 = 12
        channel_2 = 13
        channel_3 = 15
        channel_4 = 16
        channel_5 = 18
        channel_6 = 22
        channel_7 = 24
        channels = [
            channel_0, channel_1, channel_2, channel_3,
            channel_4, channel_5, channel_6, channel_7,
        ]
        return channels

    # Test cycle through channels: Test Onboard LEDs - Forward
    def forward(self):
        for channel in self.channels:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
            time.sleep(self.speed)
            GPIO.output(channel, False)

    # Test cycle through channels: Test Onboard LEDs - Reverse
    def reverse(self):
        for channel in self.channels[::-1]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
            time.sleep(self.speed)
            GPIO.output(channel, False)

    # Test cycle through channels: Test Onboard LEDs - Random
    def random_selection(self):
        for channel in [random.choice(self.channels) for _ in range(0, 128)]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
            time.sleep(self.speed)
            GPIO.output(channel, False)

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

    # Driver method
    def run(self):
        # Test pairing of lights from the outside channels to the inside and reverse
        self.outside_in()
        self.inside_out()

        # Quickly and randomly (using LCG) choose and flash lights
        self.random_selection()

        # Force a slow blink on the lights: forward and reverse
        for _ in range(5):
            self.forward()
            self.reverse()


def main():
    x = GPIOTest(speed=0.75)
    x.run()


if ((__name__) == ("__main__")):
    main()
