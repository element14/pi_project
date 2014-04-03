#!/usr/bin/env python2.7
#
#==============================================================
#
# Authors:      Christine Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 2nd April 2014
#
# Description: 
#
# This python script monitors a tilt sensor and turns an Led on/off accordingly
# It uses the GPIO output ports of the RPi to
#   - read a tilt sensor attached to O1 of a TinkerKit shield on an embeddedPi
#       (using output O1 BCM GPIO 8 as an input)
#   - switch on/off an led attached to O0 of the same Tinkerkit Shield
#       (using output O0 BCM GPIO 10 as an output)
#
# The Pin mapping is:
#   RPi BCM GPIO pin    10   8   4  23  22  18
#   embeddedPi pin      11  10   9   6   5   3
#   Tinkershield output O0  O1  O2  O3  O4  O5
#
# It keeps reading the status of the tilt sensor until either
#   - there have been 50 changes ( a change = one press or one release )
#   - or ctrl+c is pressed to exit
# When the tilt sensor reads 1 the Led on Output 0 is turned ON
# When the tilt sensor reads 0 the Led on Output 0 is turned OFF 
#
# It needs to be run as sudo ( i.e. with root priveleges)
#   sudo python epi-tilt-rgv1p0p0.py 
#
# History:      Original release.
#
# Copyright:    2014 (c) Premier Farnell Limited
#
# License:      GPLv3+
#
#==============================================================#

# import the GPIO library so we can use the 
# standard GPIO methods to access GPIO ports
import RPi.GPIO as GPIO
from time import sleep

# the embeddedPi output GPIO ports O0 to O5 are BCM port numbers 10,8,4,23,22,18
ports = [10, 8, 4, 23, 22, 18]
# we will use port O1 GPIO  8 for the tilt
#             port O0 GPIO 10 for the LED

# initialise RPi.GPIO to use BCM pin numbering
GPIO.setmode(GPIO.BCM)  

# set up tilt port for input using output O1 on the tinkershield
tilt_port_num = 8
GPIO.setup(tilt_port_num, GPIO.IN)

# set up led port for output using Output O0 on the tinkershield
led_port_num = 10
GPIO.setup(led_port_num, GPIO.OUT)
GPIO.output(led_port_num,0) # make sure led is off to start
sleep(0.21)
    
# ask user to press enter when they are ready to start
raw_input("When ready hit enter.\n")

# set intial values for variables
change_count = 0        # the number of times the tilt sensor has changed state
previous_status = ''    # the previous state of the tilt
current_status = 0      # the current  state of the tilt

# read tilt until 50 changes are made or ctrl+c pressed
try:
    while change_count < 51 :
        # read current state of tilt
        current_status = GPIO.input(tilt_port_num)
        if current_status:
            # set current status to "1" ready for printing and turn led ON
            GPIO.output(led_port_num,1)
            current_status = "1"            
        else:
            # set current status to "0" ready for printing and turn led OFF
            GPIO.output(led_port_num,0)
            current_status = "0"
        if current_status != previous_status:
            #if the tilt reading has changed then print the new state
            print (current_status ) 
            # update status variable for next comparison
            previous_status = current_status
            # increment change counter
            change_count += 1                   

except KeyboardInterrupt:       # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()              # resets all GPIO ports used by this program
GPIO.cleanup()                  # clean up GPIO ports on normal exit
