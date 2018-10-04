#!/usr/bin/python3

# Output Module. Set GPIO outputs of Raspberry Pi to display 5 colors
#
# Input is set in percentages (0-100) for warmwhite,coldwhite,red,green,blue


import RPi.GPIO as GPIO

import control



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
#   23... blue
#   24... red
#   25... green
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
    cw = GPIO.PWM(6, pwm_freq)
    red = GPIO.PWM(24, pwm_freq)
    green = GPIO.PWM(25, pwm_freq)
    blue = GPIO.PWM(23, pwm_freq)

    return (ww,cw,red,green,blue)


def start_gpio_pwm(ww,cw,red,green,blue):
# Start Pulse Width Modulation on Outputs

    ww.start(0) 

    cw.start(0) 

    red.start(0) 

    green.start(0) 

    blue.start(0) 



def stop_gpio_pwm(ww,cw,red,green,blue):
# Stop Pulse Width Modulation

    ww.stop()
    cw.stop()
    red.stop()
    green.stop()
    blue.stop()



def colors(ww,cw,red,green,blue,ww_c,cw_c,red_c,green_c,blue_c):
#set color output

    if control.extra_switch() == 1:
        ww_c = 100*ww_c / (ww_c + cw_c)
        cw_c = 100*cw_c / (ww_c + cw_c)
        print(1)
    else:
        print(0)

    ww.ChangeDutyCycle(ww_c)
    cw.ChangeDutyCycle(cw_c)
    red.ChangeDutyCycle(red_c)
    green.ChangeDutyCycle(green_c)
    blue.ChangeDutyCycle(blue_c)
