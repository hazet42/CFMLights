#!/usr/bin/python3

# Output Module. Set GPIO outputs of Raspberry Pi to display 5 colors
#
# Input is set in percentages (0-100) for warmwhite,coldwhite,red,green,blue


import RPi.GPIO as GPIO


# Initialize GPIO Ports

def init_gpio(pwm_freq):
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

    ww = GPIO.PWM(5, pwm_freq)
    ww.start(0) 

    cw = GPIO.PWM(6, pwm_freq)
    cw.start(0) 

    red = GPIO.PWM(23, pwm_freq)
    red.start(0) 

    green = GPIO.PWM(24, pwm_freq)
    green.start(0) 

    blue = GPIO.PWM(25, pwm_freq)
    blue.start(0) 

    return (ww,cw,red,green,blue)


# Set GPIO Output

#def setoutput(ww,cw,red,green,blue):
    #nothing here yet
