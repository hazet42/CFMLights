#!/usr/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#
# Load libraries to directly access Raspberry's GPIO ports:

# Import Systemwide libraries:

import RPi.GPIO as GPIO
import time
import sys, getopt
import logging


# Import application modules:

import init
import output
import control

def main(argv):
# Read Location from Config File

    logging.basicConfig(level=logging.INFO)

    init.ReadArgs(argv)
    (loc_lon,loc_lat,prog_num,pwm_freq) = init.ReadConfFile()


    # Initialize GPIO-Ports

    output.init_gpio()
     


    # Main Loop: run as long as onoff switch is set

    while True:
        if control.onoff_switch:
            # Start PWM on outputs:
            (ww,cw,red,green,blue) = output.start_gpio_pwm(pwm_freq)
        else:
            # Stop PWM:
            output.stop_gpio_pwm

        while control.onoff_switch:
            pause_time = 0.010
            green.ChangeDutyCycle(100)
            ww.ChangeDutyCycle(20)
    #        for i in range(0,100+1):
    #            cw.ChangeDutyCycle(i)
    #            ww.ChangeDutyCycle(100-i)
    #            time.sleep(pause_time)
    #        for i in range(100,-1,-1):
    #           cw.ChangeDutyCycle(i)
    #           ww.ChangeDutyCycle(100-i)
            time.sleep(pause_time)

    GPIO.cleanup()


if __name__ == "__main__":
    main(sys.argv[1:])
