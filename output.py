#!/usr/bin/python3

# Output Module. Set pulse width modulation (PWM) outputs to dim LED lights:
# Two options, as defined in the config file in pwm_mode:
#   HW ... use Adafruit Pca9685 - Bord for pulse witdh modulation
#   SW ... use Raspberry Pi's software PWM
#
# Input is set in percentages (0-100) for warmwhite,coldwhite,red,green,blue


import RPi.GPIO as GPIO
import time
import control
import board
import busio
import adafruit_pca9685



# Initialize GPIO Ports

def init_gpio(pwm_freq):
# Set the GPIO outputs to be GPIO numbers (instead of board pin numbers):

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

# Define GPIO output Channels if SW PWM is selected: 
#
#    5... warmwhite
#    6... coldwhite
#
#   23... blue
#   24... red
#   25... green

    if pwm_mode == "SW":
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)

        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(24, GPIO.OUT)
        GPIO.setup(25, GPIO.OUT)

        ww = GPIO.PWM(5, pwm_freq)
        cw = GPIO.PWM(6, pwm_freq)
        red = GPIO.PWM(24, pwm_freq)
        green = GPIO.PWM(25, pwm_freq)
        blue = GPIO.PWM(23, pwm_freq)



    elif pwm_mode == "HW":
        i2c = busio.I2C(board.SCL, board.SDA)
        hat = adafruit_pca9685.PCA9685(i2c)
        hat.frequency = pwm_freq

        red = hat.channels[6]
        blue = hat.channels[5]
        green = hat.channels[4]
        cw = hat.channels[0]
        ww = hat.channels[1]



    gpio=(ww,cw,red,green,blue)

# Set Input GPIO channels for switching
# Inputs are pulled DOWN, so they expect 3.3V to be HIGH
#   12... switch on-off
#   13... switch sunlight-extralight

    GPIO.setup(12, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(13, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

    return (gpio)


def start_gpio_pwm(gpio):
# Start Pulse Width Modulation on Outputs

    (ww,cw,red,green,blue)=gpio

    if pwm_mode == "SW":
        ww.start(0) 
        cw.start(0) 
        red.start(0) 
        green.start(0) 
        blue.start(0) 



def stop_gpio_pwm(gpio):
# Stop Pulse Width Modulation

    (ww,cw,red,green,blue)=gpio

    if pwm_mode == "SW":
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



def hexscale(color):

    # Software-Module requires duty cycles between 0 ... 0xfff
    # this function scales the percentage value (0 ... 100%) to this range

    colorhex = color/100*0xffff
    return (colorhex)



def colors(gpio,wcrgb):
#set color output

    (ww,cw,red,green,blue)=gpio
    (ww_c,cw_c,red_c,green_c,blue_c) = wcrgb

    if pwm_mode == "HW":
        ww.ChangeDutyCycle(ww_c)
        cw.ChangeDutyCycle(cw_c)
        red.ChangeDutyCycle(red_c)
        green.ChangeDutyCycle(green_c)
        blue.ChangeDutyCycle(blue_c)

    elif pwm_mode == "SW":
        ww.duty_cycle = hexscale(ww_c)
        cw.duty_cycle = hexscale(cw_c)
        red.duty_cycle = hexscale(red_c)
        green.duty_cycle = hexscale(green_c)
        blue.duty_cycle = hexscale(blue_c)

    else:
        print("pwm_mode error")
