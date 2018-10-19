#!/usr/bin/python3

# Program Module. Creates color programs
#

from pysolar.solar import *
import datetime


def calc_color(loc_lat, loc_lon, date):
# calculate the color
        altitude_deg = get_altitude(loc_lat, loc_lon, date)
        if altitude_deg < -10:
            brightness = 0
            red = 5
            green = 0
            blue = 10
        elif altitude_deg < -3:
            brightness = 0
            red = 0
            green = 0
            blue = (altitude_deg+10)/7*10
        elif altitude_deg < 1:
            if altitude_deg > 0:
                brightness = radiation.get_radiation_direct(date, altitude_deg)
            else:
                # pySolar cannot handle radiation for altitudes <= 0:
                brightness = 0
            red = (altitude_deg+3)/4*10
            green = red/4
            blue = (1-(altitude_deg+3)/4)*10
        elif altitude_deg<10:
            brightness = radiation.get_radiation_direct(date, altitude_deg)
            red = 10 + (altitude_deg-1)/9*90
            green = red/3 
            blue = 0
        elif altitude_deg < 15:
            brightness = radiation.get_radiation_direct(date, altitude_deg)
            red = 100
            green = (altitude_deg - 10)/5*100
            blue = (altitude_deg - 10)/5*100
        else:
            brightness = radiation.get_radiation_direct(date, altitude_deg)
            red = 80
            green = 80
            blue = 100
        
        maxbrightness = 500
        if altitude_deg < 15:
            whiteness = altitude_deg/15*brightness/maxbrightness * 100
            warmness = (1-altitude_deg/15)*brightness/maxbrightness * 100
        else:
            whiteness = brightness/maxbrightness*100
            warmness = 0

        whiteness = min(100,max(0,whiteness))
        warmness = min(100,max(0,warmness))
        red = min(100,max(0,red))
        green = min(100,max(0,green))
        blue = min(100,max(0,blue))

        wcrgb = [warmness,whiteness,red,green,blue]

        return (wcrgb)

def colors(prog_num,loc_lon,loc_lat):
# Select the program for the WW/CW RGB Values. This is the switcher, the programs are defines above
    if prog_num == 0:    
        wcrgb = [0,0,100,0,0]

    elif prog_num == 1:
        wcrgb = [50,50,50,50,100]

    elif prog_num == 2:
        # Simulate the radiation of the sun at position (loc_lon,loc_lat) at the time NOW
        date = datetime.datetime.now()
        wcrgb = calc_color(loc_lat, loc_lon, date)

    elif prog_num == 3:
        # Simulate radiation of the sun in fast forward
        date = datetime.datetime.now()
        date_ff = datetime.datetime(date.year,date.month,date.day,int(date.minute/60*24),date.second,0,tzinfo=datetime.timezone.utc)
        wcrgb = calc_color(loc_lat, loc_lon, date_ff)

    return (wcrgb)


