#!/usr/bin/python3

# Output Module. Set GPIO outputs of Raspberry Pi to display 5 colors
#
# Input is set in percentages (0-100) for warmwhite,coldwhite,red,green,blue


import RPi.GPIO as GPIO
import time
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

    gpio=(ww,cw,red,green,blue)

    return (gpio)


def start_gpio_pwm(gpio):
# Start Pulse Width Modulation on Outputs

    (ww,cw,red,green,blue)=gpio

    ww.start(0) 
    cw.start(0) 
    red.start(0) 
    green.start(0) 
    blue.start(0) 



def stop_gpio_pwm(gpio):
# Stop Pulse Width Modulation

    (ww,cw,red,green,blue)=gpio

    ww.stop()
    cw.stop()
    red.stop()
    green.stop()
    blue.stop()


def fade_color(gpio,wcrgb_old,wcrgb):

    (ww_c,cw_c,red_c,green_c,blue_c) = wcrgb
    (ww_o,cw_o,red_o,green_o,blue_o) = wcrgb_old

    #calculate step size to reach new colors after 100 steps:

    ww_d = (ww_c - ww_o)/100
    cw_d = (cw_c - cw_o)/100
    red_d = (red_c - red_o)/100
    green_d = (green_c - green_o)/100
    blue_d = (blue_c - blue_o)/100


    #cycle old to new:

    for i in range (0,100):
        wcrgb_i = [ww_o + i*ww_d, cw_o + i*cw_d, red_o + i*red_d, green_o + i*green_d, blue_o + i*blue_d]
        colors(gpio,wcrgb_i)
        time.sleep(0.01)

    colors(gpio,wcrgb)

    return (wcrgb)



def colors(gpio,wcrgb):
#set color output

    (ww,cw,red,green,blue)=gpio
    (ww_c,cw_c,red_c,green_c,blue_c) = wcrgb

    ww.ChangeDutyCycle(ww_c)
    cw.ChangeDutyCycle(cw_c)
    red.ChangeDutyCycle(red_c)
    green.ChangeDutyCycle(green_c)
    blue.ChangeDutyCycle(blue_c)
