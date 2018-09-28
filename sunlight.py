#!/usr/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#
# Load libraries to directly access Raspberry's GPIO ports:

import RPi.GPIO as GPIO
import time
import sys, getopt
import init


def main(argv):
# Read Location from Config File

    init.ReadArgs(argv)
    init.ReadConfFile


# Set the GPIO outputs to be GPIO numbers (instead of board pin numbers):

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


# Define GPIO Channels (mainly use the ones that do not have additional functionality):
# Inputs are pulled DOWN, so they expect 3.3V to be HIGH
#
#    5... warmwhite
#    6... coldwhite
#
#   23... red
#   24... green
#   25... blue
#
#   12... switch on-off
#   13... switch sunlight-extralight

    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)

    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)

    GPIO.setup(12, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(13, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
     
    red_led = GPIO.PWM(5,100)
    red_led.start(0)


# Test PWM 
    while True:
        pause_time = 0.010
        for i in range(0,100+1):
            red_led.ChangeDutyCycle(i)
            time.sleep(pause_time)
        for i in range(100,-1,-1):
            red_led.ChangeDutyCycle(i)
            time.sleep(pause_time)

    GPIO.cleanup()

#    GPIO.output(5,True)
#    time.sleep(1)
#    GPIO.output(5,False)
#    time.sleep(1)


# not much more yet...

    print("Hello World")


if __name__ == "__main__":
    main(sys.argv[1:])
