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


def main(argv):
# Read Location from Config File

    logging.basicConfig(level=logging.INFO)

    init.ReadArgs(argv)
    (loc_lon,loc_lat,prog_num,pwm_freq) = init.ReadConfFile()


# Initialize GPIO-Ports

    (ww,cw,red,green,blue) = output.init_gpio(pwm_freq)
     


# Test PWM 
    while True:
        pause_time = 0.010
        for i in range(0,100+1):
            red.ChangeDutyCycle(i)
            time.sleep(pause_time)
        for i in range(100,-1,-1):
            red.ChangeDutyCycle(i)
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
