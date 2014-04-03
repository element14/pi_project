#!/usr/bin/env python3.2
#==============================================================
#
# Authors:      Christine Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 25th March 2014
#
# Description: 
#
# This python script uses the GPIO output ports of the RPi to control leds
# attached to a TinkerKit shield on an embeddedPi (outputs O0 to O5)
# The Pin mapping is:
#   RPi BCM GPIO pin    10   8   4  23  22  18
#   embeddedPi pin      11  10   9   6   5   3
#   Tinkershield output O0  O1  O2  O3  O4  O5
#
#
# Thanks to Alex Eames, Gert Jan van Loo & Myra VanInwegen
# for their python scripts used in the making of this script.
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
# import the 'sleep' method so we can wait between tests
from time import sleep

# define  constants for clarity
led_OFF = 0
led_ON  = 1
all_at_once  = 1
individually = 0

# tinkershied ports O0 to O5 are embeddedpi ports 11,10,9,6,5,3 
# which are BCM ports 10,8,4,23,22,18 on the R-Pi

ports = [10, 8, 4, 23, 22, 18]
ports_rev = ports[:]                            # make a copy of ports list
ports_rev.reverse()                             # and reverse it as we need both
GPIO.setmode(GPIO.BCM)                          # initialise RPi.GPIO

# setup the ports for outputand make sure LEDs are off before we start
for port_num in ports:
    GPIO.setup(port_num, GPIO.OUT)              # set up ports for output
    GPIO.output(port_num, led_OFF)              # make sure all off first
    sleep(0.21)
    
# ******* define a method 'led_drive' to generate led test patterns **********
#   reps        = the number of times to repeat the sequence
#   multiple    = 1 if leds are to remain on so multiple leds lit at once
#               = 0 means led will be turned off before proceeding to next led
#   direction   = an array containing the port numbers
#                   in this python script we have declared two arrays
#                   ports containing the pin numbers in forwards order O0 to O5
#                   ports_rev containing pin numbers in reverse  order O5 to O0
                    
def led_drive(reps, multiple, direction):       # define function to drive leds
    for i in range(reps):
        for port_num in direction:              
            GPIO.output(port_num, led_ON)       # switch on an led
            sleep(0.21)                         # wait for ~0.21 seconds
            if not multiple:                    # if we're not leaving it on
                GPIO.output(port_num, led_OFF)  # switch it off

raw_input("When ready hit enter.\n")
# now use that method to generate multiple test patterns
try:
    # turn on then off each led in turn in order O0 to O5 three times
    led_drive(3, individually, ports)                  
    # turn on then off each led in turn in reverse order O5 to O0 three times
    led_drive(3, individually, ports_rev)
    sleep(0.21)
    # turn on each port so all on
    led_drive(1, all_at_once, ports)
    sleep(0.21)
    # turn all on in turn so all on at once, then turn off
    led_drive(1, all_at_once , ports)
    sleep(0.21)
    led_drive(1, individually, ports)        
    sleep(0.21)
    # turn all on in reverse order so all on at once then turn off
    led_drive(1, all_at_once , ports_rev)
    sleep(0.21)
    led_drive(1, individually, ports)
    sleep(0.21)
    
except KeyboardInterrupt:                   # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()                          # clean up GPIO ports on CTRL+C

GPIO.cleanup()                              # clean up GPIO ports on normal exit
