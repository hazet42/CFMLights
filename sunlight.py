#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#
# Load libraries to directly access Raspberry's GPIO ports:

import RPi.GPIO as GPIO
import time
import sys, getopt
import ConfigParser

# functions
# Read Command line arguments

def main(argv):
   global verbose 
   verbose = False
   try:
      opts, args = getopt.getopt(argv,"vh")
   except getopt.GetoptError:
      print 'sunlight.py -h to display options'
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h':
          print 'sunlight.py -v for verbosity'
          sys.exit()
       elif opt in ("-v"):
          verbose = True


if __name__ == "__main__":
       main(sys.argv[1:])

# Enable verbosity:
if verbose :
    def verboseprint(*args):
        # Print each argument separately so caller doesn't need to
        # stuff everything to be printed into a single string
        for arg in args:
           print arg,
        print
else:   
   verboseprint = lambda *a: None      # do-nothing function


# ---------------------------------------------------------------
# Main


# Read Location from Config File

config = ConfigParser.RawConfigParser()
config.read('CFMLights.cfg')

loc_lon = config.getfloat('Location', 'Longitudinal')
loc_lat = config.getfloat('Location', 'Latitudinal')
verboseprint("Configfile options: Location lon: ", loc_lon,", lat: ",loc_lat)


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
#   12... switch white
#   13... switch color

GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

GPIO.setup(12, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
 

# Test Routine: set on / off for 1 second:

state = True
 
# endless loop, on/off for 1 second
while True:
	GPIO.output(5,True)
	time.sleep(1)
	GPIO.output(5,False)
	time.sleep(1)


# not much more yet...

print "Hello World"
