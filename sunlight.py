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

    pause_time = 0.10

    # Initialize GPIO-Ports

    (ww,cw,red,green,blue) = output.init_gpio(pwm_freq)


    # Main Loop: run as long as onoff switch is set

    while True:
        if control.onoff_switch() == 1: 
            # Start PWM on outputs:
            output.start_gpio_pwm(ww,cw,red,green,blue)

            while control.onoff_switch() == 1:
                pause_time = 0.10
            
                output.colors(ww,cw,red,green,blue,10,0,0,0,60)

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
            output.stop_gpio_pwm(ww,cw,red,green,blue)

        time.sleep(pause_time)

    GPIO.cleanup()


if __name__ == "__main__":
    main(sys.argv[1:])
