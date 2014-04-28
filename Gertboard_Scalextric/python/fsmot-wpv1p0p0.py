#!/usr/bin/python2.7

# this program controls the motor of a scalextric

from __future__ import print_function       
from time import sleep
                        
import wiringpi
import sys
import termios
import tty

board_type = sys.argv[-1]
#define variables for getting input from keyboard
old_attributes="OLD"
inkey_buffer=1

# function to read just 1 key press
# NB.An inkey_buffer value of 0, zero, generates a "" character and carries on 
# instead of waiting for a valid ASCII key press.
def inkey():
    fd=sys.stdin.fileno() 
    old_attributes=termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    character=sys.stdin.read(inkey_buffer)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_attributes)
    return character

# Set up the GPIO system to drive the motor using PWM
# Note we are using GPIO.BCM pin numbering
def setup_ports():
    wiringpi.wiringPiSetupGpio()                # Initialise wiringpi GPIO
    wiringpi.pinMode(18,2)                      # Set up GPIO 18 to PWM mode
    wiringpi.pinMode(17,1)                      # GPIO 17 to output
    wiringpi.digitalWrite(17, 0)                # port 17 off for rotation one way
    wiringpi.pwmWrite(18,0)                     # set pwm to zero initially

# function to reset the ports for a safe exit
def reset_ports():
    wiringpi.pwmWrite(18,0)                 # set pwm to zero
    wiringpi.digitalWrite(18, 0)            # ports 17 & 18 off
    wiringpi.digitalWrite(17, 0)
    wiringpi.pinMode(17,0)                  # set ports back to input mode
    wiringpi.pinMode(18,0)

#  function to handle the display bar nnnn #####
# where nnnn is the current PWM value and this is followed by
# a string of characters - one per 16 of PWM value, plus enough spaces to make up to 64 characters
#   char = the character to be used in the bar
#   pwm_value = the PWM value to be displayed (in format nnnn as beginning of line)
def display(char, pwm_value):        
    reps = pwm_value/16
    spaces = 64 - reps
    print ('\r',"{0:04d}".format(pwm_value), ' ', char * reps, ' ' * spaces,'\r', sep='', end='') 
    sys.stdout.flush()

char = '#'                  # define the bar chart character 
pwm = 0                     # pulse width modulation value initialised to 0
old_pwm = 0                 # value fo pwm last time through loop
pwm_increment = 0           # value to add or subtract from pwm when faster to slower pressed
max_PWM = 1023
min_PWM = 0

print(" WELCOME TO THE SCALEXTRIC CONTROLLER\n")
print ("These are the connections for controlling the scalextric motor:")

if board_type == "m":
    print ("   GPIO 17 --- MOTB")
    print ("   GPIO 18 --- MOTA")
    print ("   + of external power source --- MOTOR +")
    print ("   ground of external power source --- MOTOR - ")
    print ("   one wire for your motor in MOTOR A screw terminal")
    print ("   the other wire for your motor in MOTOR B screw terminal")

else:
    print ("   GP17 in J2 --- MOTB (just above GP1)")
    print ("   GP18 in J2 --- MOTA (just above GP4)")
    print ("   + of external power source --- MOT+ in J19")
    print ("   ground of external power source --- GND (any)")
    print ("   one wire for your motor in MOTA in J19")
    print ("   the other wire for your motor in MOTB in J19")
print("")
print("Whilst running, the display bar shows current PWM figure in range 0 to 1023\n")
print("Press f to go faster, s to go slower, ESC to exit")
print("")

# ask user to choose an increment to add or subtract from PWM for faster and slower
while pwm_increment <1:
    try:
        pwm_increment = int(raw_input("Choose an increment value in range 1-200 : "))
        if pwm_increment >200:
            print("\n Too big ,  must be in range 1-200 please!")
            pwm_increment = 0
        elif pwm_increment < 1:
            print("\n Too small ,  must be in range 1-200 please!")
            pwm_increment = 0
    except ValueError:
        pwm_increment = 0
        print("\nInteger number in range 1-200 only please!")

raw_input("Hit <RETURN/ENTER> to begin...\n ")

setup_ports()
display(char,pwm)
try:
    while True:
        # Use the INKEY function to grab an ASCII key.
        character=inkey()
        # f or F means go faster
        if character=="f" or character=="F":
            pwm += pwm_increment
        # s or S means go slower
        if character=="s" or character=="S":
            pwm -= pwm_increment
        # Esc key to exit the loop...
        if character==chr(27): break
        # ignore any other key
        if pwm > max_PWM: pwm = max_PWM
        if pwm < min_PWM: pwm = min_PWM
        if pwm != old_pwm:
            # send PWM value to port 18
            wiringpi.pwmWrite(18, pwm)   
            old_pwm = pwm
            # workout format of display bar and print to screen
            display(char, pwm)
        # sleep before looking for a key press again
        sleep(0.05)

except KeyboardInterrupt:                   # trap a CTRL+C keyboard interrupt
    reset_ports()
    print ("\nRun interrupted")

reset_ports()

print("\n Run finished")
