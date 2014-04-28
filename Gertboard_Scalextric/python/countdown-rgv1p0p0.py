#!/usr/bin/env python
#==============================================================
#
# Authors:      Christine Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 15th April 2014
#
# Description:
# This python script runs a set of countdown LEDs started on a button press
# using the RPi.GPIO library.
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
import RPi.GPIO as GPIO
import sys
from time import sleep

button = 25
red_led = 24
yellow_led = 23
green_led = 22
led_ON  = 1
led_OFF = 0

# initialise all ports first
GPIO.setmode(GPIO.BCM)              # initialise GPIO to use BCM_GPIO port numbers
GPIO.setup(button, GPIO.IN)         # set up button port for input
GPIO.setup(red_led, GPIO.OUT)       # set up red LED port for output
GPIO.setup(yellow_led, GPIO.OUT)    # set up yellow LED port for output    
GPIO.setup(green_led, GPIO.OUT)     # set up green LED port for output
GPIO.output(red_led, led_OFF)       # make sure red led is off to start
GPIO.output(yellow_led, led_OFF)    # make sure yellow led is off to start
GPIO.output(green_led, led_OFF)     # make sure green led is off to start

def reset_ports():                  # resets the ports for a safe exit
    GPIO.setup(button,GPIO.IN)      # set button port to input mode
    GPIO.setup(red_led,GPIO.IN)     # set red led port to input mode
    GPIO.setup(yellow_led,GPIO.IN)  # set yellow led port to input mode
    GPIO.setup(green_led,GPIO.IN) # set green led port to input mode

# wait for the button to be pressed
print("\nPress button to start countdown")
try:
    while GPIO.input(button)== 1:
        sleep(0.1)
    print("\nStarting countdown")
    # STOP  : turn on red LED
    GPIO.output(red_led, led_ON)
    sleep (2)
    # READY : turn Yellow on
    GPIO.output(yellow_led, led_ON)
    sleep (2)
    # STEADY: blink red & yellow LEDs
    for i in range (0,10):
        GPIO.output(red_led, led_OFF)
        GPIO.output(yellow_led, led_OFF)
        sleep(0.1)
        GPIO.output(red_led, led_ON)
        GPIO.output(yellow_led, led_ON)
        sleep(0.1)
    # GO    : turn red & Yellow LEDs off and Green LED on
    GPIO.output(red_led, led_OFF)
    GPIO.output(yellow_led, led_OFF)
    GPIO.output(green_led, led_ON)
    sleep (6)
    # turn Green LED off
    GPIO.output(green_led, led_OFF)

    reset_ports()           # on finishing,reset all GPIO ports used by this program
    print("\nCountdown complete\n")
    
except KeyboardInterrupt:                 # trap a CTRL+C keyboard interrupt
    print("\nCtrl^C pressed. Exiting without Countdown\n")
    reset_ports()                         # resets GPIO ports
