#!/usr/bin/env python
#==============================================================
#
# Authors:      Christine Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 15th April 2014
#
# Description:
# This python script runs a set of countdown LEDs started on a button press
# using the wiringpi library
#   sets up gpio.BCM port 25 as a button
#   sets up port 24 as the Red LED
#   sets up port 23 as the Yellow LED
#   sets up port 22 as the Green LED
#   waits for a button press
#   turns on red LED for 2 secs
#   turns on yellow LED & waits 2 secs so both red and yellow on together 2 secs
#   blinks red and yellow LEDs together for 2 secs
#   turns off yellow & Red LEDS then turns on Green LED for 6 seconds.
#   resets gpio ports for safe exit
#
# History:      Original release.
#
# Copyright:    2014 (c) Premier Farnell Limited
#
# License:      GPLv3+
#
#==============================================================#
import wiringpi
import sys
from time import sleep
#board_type = sys.argv[-1]

button = 25
red_led = 24
yellow_led = 23
green_led = 22
led_ON  = 1
led_OFF = 0

# initialise all ports first
wiringpi.wiringPiSetupGpio()        # initialise wiringpi to use BCM_GPIO port numbers
wiringpi.pinMode(button, 0)         # set up button port for input
wiringpi.pullUpDnControl(button, wiringpi.PUD_UP)   # set button port as pullup
wiringpi.pinMode(red_led, 1)        # set up red LED port for output
wiringpi.pinMode(yellow_led, 1)     # set up yellow LED port for output    
wiringpi.pinMode(green_led, 1)      # set up green LED port for output
wiringpi.digitalWrite(red_led, led_OFF)     # make sure red led is off to start
wiringpi.digitalWrite(yellow_led, led_OFF)  # make sure yellow led is off to start
wiringpi.digitalWrite(green_led, led_OFF)   # make sure green led is off to start

def reset_ports():                          # resets the ports for a safe exit
    wiringpi.pullUpDnControl(22, wiringpi.PUD_OFF) #unset pullup on button port
    wiringpi.pinMode(button,0)              # set button port to input mode
    wiringpi.pinMode(red_led,0)             # set red led port to input mode
    wiringpi.pinMode(yellow_led,0)          # set yellow led port to input mode
    wiringpi.pinMode(green_led,0)           # set red led port to input mode

# wait for the button to be pressed
print("\nPress button to start countdown")
try:
    while wiringpi.digitalRead(button)== 1:
        sleep(0.1)
    print("\nStarting countdown")
    # STOP  : turn on red LED
    wiringpi.digitalWrite(red_led, led_ON)
    sleep (2)
    # READY : turn Yellow on
    wiringpi.digitalWrite(yellow_led, led_ON)
    sleep (2)
    # STEADY: blink red & yellow LEDs
    for i in range (0,10):
        wiringpi.digitalWrite(red_led, led_OFF)
        wiringpi.digitalWrite(yellow_led, led_OFF)
        sleep(0.1)
        wiringpi.digitalWrite(red_led, led_ON)
        wiringpi.digitalWrite(yellow_led, led_ON)
        sleep(0.1)
    # GO    : turn red & Yellow LEDs off and Green LED on
    wiringpi.digitalWrite(red_led, led_OFF)
    wiringpi.digitalWrite(yellow_led, led_OFF)
    wiringpi.digitalWrite(green_led, led_ON)
    sleep (6)
    # turn Green LED off
    wiringpi.digitalWrite(green_led, led_OFF)

    reset_ports()           # on finishing,reset all GPIO ports used by this program
    print("\nCountdown complete\n")
    
except KeyboardInterrupt:                 # trap a CTRL+C keyboard interrupt
    print("\nCtrl^C pressed. Exiting without Countdown\n")
    reset_ports()                         # resets GPIO ports
