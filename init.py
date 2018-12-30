#!/usr/bin/python3

import sys, getopt
import configparser


global verbose,pwm_freq,pwm_mode
verbose = False

# Read CommandLineArguments

def ReadArgs(argv):
   try:
      opts, args = getopt.getopt(argv,"vh")
   except getopt.GetoptError:
      print('sunlight.py -h to display options')
      sys.exit(2)
   for opt, arg in opts:
       if opt == '-h':
          print('sunlight.py -v for verbosity')
          sys.exit()
       elif opt in ("-v"):
          verbose = True


# Read Location from Config File

def ReadConfFile():
    config = configparser.RawConfigParser()
    config.read('CFMLights.cfg')

    # Read Geo-Information and Standard-Program Number from Config File
    
    loc_lon = config.getfloat('Location', 'Longitudinal')
    loc_lat = config.getfloat('Location', 'Latitudinal')
    prog_num = config.getint('Programs', 'Startprogram')

    
    # Read Output Parameters from config file and store in global variables

    globals()['pwm_freq'] = config.getint('Output', 'PWMFrequency')
    globals()['pwm_mode'] = config.get('Output', 'PWMMode')

    return (loc_lon,loc_lat,prog_num)

# Enable verbosity:

if verbose :
        def verboseprint(*args):
            # Print each argument separately so caller doesn't need to
            # stuff everything to be printed into a single string
            for arg in args:
                           print(arg,)
            print
else:
        verboseprint = lambda *a: None      # do-nothing function
