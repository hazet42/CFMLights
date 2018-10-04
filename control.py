#!/usr/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#
# Read hardware input / web input

# Import Systemwide libraries:

import RPi.GPIO as GPIO

# Import application modules:


# for now (since hardware switches and web switch are not existend):

def onoff_switch():
    onoff_state = GPIO.input(12)
    return onoff_state

def extra_switch():
    extra_state = GPIO.input(13)
    return extra_state
