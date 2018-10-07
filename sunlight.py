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
import program

def main(argv):
# Read Location from Config File

    logging.basicConfig(level=logging.INFO)

    init.ReadArgs(argv)
    (loc_lon,loc_lat,prog_num,pwm_freq) = init.ReadConfFile()

    pause_time = 0.10

    # Initialize GPIO-Ports

    gpio = output.init_gpio(pwm_freq)


    # Set Color Start Values

    wcrgb_old = [0,0,0,0,0]
    wcrgb = [0,0,0,0,0]


    # Set Starting Program (TODO: should be read out of config-file - Issue 23)

    prognr = 0 


    # Main Loop: run as long as onoff switch is set

    while True:
        if control.onoff_switch() == 1: 
            # Start PWM on outputs:
            output.start_gpio_pwm(gpio)

            while control.onoff_switch() == 1:
                pause_time = 0.10
            
               
                wcrgb = program.colors(prognr)
                if control.extra_switch() == 1:
                    wcrgb[0] = 100*wcrgb[0] / (wcrgb[0] + wcrgb[1])
                    wcrgb[1] = 100*wcrgb[1] / (wcrgb[0] + wcrgb[1])

                wcrgb_old = output.fade_color(gpio,wcrgb_old,wcrgb)

                time.sleep(pause_time)
        #        for i in range(0,100+1):
        #            cw.ChangeDutyCycle(i)
        #            ww.ChangeDutyCycle(100-i)
        #            time.sleep(pause_time)
        #        for i in range(100,-1,-1):
        #           cw.ChangeDutyCycle(i)
        #           ww.ChangeDutyCycle(100-i)

        else:
            # Stop PWM:
            wcrgb = [0,0,0,0,0]
            wcrgb_old = output.fade_color(gpio,wcrgb_old,wcrgb)
            wcrgb_old = [0,0,0,0,0]
            output.stop_gpio_pwm(gpio)

        time.sleep(pause_time)

    GPIO.cleanup()


if __name__ == "__main__":
    main(sys.argv[1:])
