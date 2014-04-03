#!/usr/bin/env python2.7
#
#==============================================================
#
# Authors:      Christine Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 25th March 2014
#
# Description: 
#
# This python script takes GB_Python script buttons-rg.py and adapts
# it to use the GPIO output ports of the RPi to read buttons attached to a
# TinkerKit shield on an embeddedPi (using outputs O0 to O5 as inputs)
#
# The Pin mapping is:
#   RPi BCM GPIO pin    10   8   4  23  22  18
#   embeddedPi pin      11  10   9   6   5   3
#   Tinkershield output O0  O1  O2  O3  O4  O5
#
# It keeps reading the status of the buttons until either
#   - there have been 20 changes ( a change = one press or one release )
#   - or ctrl+c is pressed to exit
# It prints the button status' when a change occurs in the form xxxxxx
# where x is the state of a button 0 = pressed, 1 = released
# eg no buttons pressed = 111111
#   first button pressed = 011111
#   then released        = 111111
#   last button pressed = 111110
#   then released       = 111111
#   second and fifth buttons pressed = 101101
#   then second button released      = 111101
#   then fifth button released       = 111111
#
# Thanks to Alex Eames, Gert Jan van Loo & Myra VanInwegen
# for their python scripts used in the making of this script.
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

# initialise RPi.GPIO to use BCM pin numbering
GPIO.setmode(GPIO.BCM)  

# set up ports for input
for port_num in ports:
    GPIO.setup(port_num, GPIO.IN)
    sleep(0.21)
    
raw_input("When ready hit enter.\n")

# set intial values for variables
button_press = 0        
previous_status = ''
status_list= [0,0,0,0,0,0]


# read buttons until 20 changes are made or ctrl+c pressed
try:
    while button_press < 21:                     
    	for i in range(0,6):
            status_list[i] = GPIO.input(ports[i])
            if status_list[i]:
                # set status to "1" ready for printing
                status_list[i] = "1"
            else:
                # set status to "0" ready for printing
                status_list[i] = "0"
        # dump current status values in a variable
        current_status = ''.join((status_list[0],status_list[1],status_list[2],status_list[3],status_list[4],status_list[5]))
        # if that variable not same as last time 
        if current_status != previous_status:
            #if the any of the buttons have changed then print the new states
            print current_status                # print the results 
            # update status variable for next comparison
            previous_status = current_status
            button_press += 1                   # increment button_press counter

except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()                 # resets all GPIO ports used by this program
GPIO.cleanup()                              # clean up GPIO ports on normal exit
