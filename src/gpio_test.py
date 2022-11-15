#!/usr/bin/python3
import RPi.GPIO as GPIO
import random
import time


class GPIOTest(object):

    def __init__(self, speed=0.05):
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
        for channel in [random.choice(self.channels) for _ in range(0, 32)]:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, True)
            time.sleep(self.speed)
            GPIO.output(channel, False)

    # Driver method
    def run(self):
        self.forward()
        self.reverse()
        self.random_selection()


def main():
    x = GPIOTest(speed=0.05)
    x.run()


if ((__name__) == ("__main__")):
    main()
