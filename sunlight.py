#!/usr/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#
# Main Module.
# Control RGB + warm white + cold white LED chains in the living room
# and pretend the color of the sun outside
#
# Uses a raspberry pi + external MosFET drivers to control the LEDs
#
# See hardware setup and wiring diagram in github's Wiki:
#   https://github.com/hazet42/CFMLights/wiki
#
# (c) 2018 by Thomas Herzinger
# Licensed under the GNU General Public License Version 3
#
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

    prognr = 2


    # Main Loop: run as long as onoff switch is set

    while True:
        if control.onoff_switch() == 1: 
            # Start PWM on outputs:
            output.start_gpio_pwm(gpio)

            while control.onoff_switch() == 1:
                pause_time = 0.50
            
               
                wcrgb = program.colors(prognr,loc_lon,loc_lat)
                if control.extra_switch() == 1:
                    if wcrgb[0]+wcrgb[1] == 0:
                        wcrgb[0] = 100
                    else:
                        wcrgb[0] = 100*wcrgb[0] / (wcrgb[0] + wcrgb[1])
                        wcrgb[1] = 100*wcrgb[1] / (wcrgb[0] + wcrgb[1])


                
                # only update PWM when changes are > 1:

#                print (wcrgb,wcrgb_old)
                
                diff = ((wcrgb[0]-wcrgb_old[0])**2+(wcrgb[1]-wcrgb_old[1])**2
                        +(wcrgb[2]-wcrgb_old[2])**2+(wcrgb[3]-wcrgb_old[3])**2
                        +(wcrgb[4]-wcrgb_old[4])**2)

                if diff > 0:
                    wcrgb_old = output.fade_color(gpio,wcrgb_old,wcrgb)

                time.sleep(pause_time)

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
