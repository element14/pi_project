#!/usr/bin/env python2.7
#
#==============================================================
#
# Authors:      Christine Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 31st March 2014
#
# Description: 
#
# This python script controls a relay by button presses
# It uses the GPIO output ports of the RPi to
#   - read a button attached to O3 of a TinkerKit shield on an embeddedPi
#       (using output O2 BCM GPIO 4 as an input)
#   - switch a relay attached to O2 of the same Tinkerkit Shield
#       (using output O3 BCM GPIO 23 as an output)
# There is a sleep of 100ms between button checks to get a clean read.
#
# The Pin mapping is:
#   RPi BCM GPIO pin    10   8   4  23  22  18
#   embeddedPi pin      11  10   9   6   5   3
#   Tinkershield output O0  O1  O2  O3  O4  O5
#
# It keeps reading the status of the buttons until either
#   - the button has been pressed 20 times 
#   - or ctrl+c is pressed to exit
# When the button is pressed the script toggles the relay-
# so if the relay was OFF it is turned ON, if it was ON it is turned OFF
#
# It needs to be run as sudo ( i.e. with root priveleges)
#   sudo python epi-relay-rgv1p0p0.py 
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
ON  = 1
OFF = 0

# initialise RPi.GPIO to use BCM pin numbering
GPIO.setmode(GPIO.BCM)  

# set up button port for input
# we will use port O2 GPIO 4 for the button
button_port_num = 4
GPIO.setup(button_port_num, GPIO.IN)

# set up relay port for output
# we will use port O3 GPIO 23 for the relay
relay_port_num = 23
GPIO.setup(relay_port_num, GPIO.OUT)
GPIO.output(relay_port_num,0) # make sure relay is off to start
sleep(0.21)
    
# wait for user to say start
raw_input("When ready hit enter.\n")

# set intial values for variables
button_press = 0        # number of button presses so far
previous_status = OFF   # the state of the button last time through the loop
current_status = OFF    # the state of the button now
relay_status = OFF      # the state of the relay

# read button until it has been pressed 20 times or ctrl+c pressed
try:
    while button_press < 21 :
        # read the current state of the button
        current_status = GPIO.input(button_port_num)
        if current_status == ON and previous_status == OFF:
            # button has been pressed so toggle relay
            if relay_status == OFF:
                #relay was OFF so turn ON
                relay_status = ON
            elif relay_status == ON:
                #relay was ON so turn OFF
                relay_status = OFF
            GPIO.output(relay_port_num,relay_status)
            button_press += 1
        # update status variable for next comparison
        previous_status = current_status
        # sleep to ensure a clean read of the button
        sleep(.1)


except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()                 # resets all GPIO ports used by this program
GPIO.cleanup()                              # clean up GPIO ports on normal exit
