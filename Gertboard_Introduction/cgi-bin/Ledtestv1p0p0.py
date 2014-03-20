#!/usr/bin/env python2.7

#==============================================================
#
# Authors:      Christine Smythe and Jenny Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 21st February 2014
#
# Description:  This Python program is designed to be called from a browser.
#               It is an adaptation of the program leds-wp.py by Alex Eames of http://RasPi.TV 
#               who based his on the leds test by Gert Jan van Loo & Myra VanInwegen.
#               It runs test sequences on the LEDs
#               This programs structure:
#                   checks which version board is in use to determine which pins to use
#                   exports the LED GPIO pins and sets them to output
#                   prints the browser page headings
#                   runs 4 test sequences
#                   turns off all the LEDs and unexports the LED GPIO pins
#                   prints the test buttons
#
# History:      Original release.
#
# Copyright:    2014 (c) Premier Farnell Limited
#
# License:      GPLv3+
#
#==============================================================

# import cgi and cgitb to enable python error messages to be sent to browser window
import cgi
import cgitb
from time import sleep

import sys          # so we can get the board type/revision
import os           # so we can make gpio calls export, unexport and write

board_type = sys.argv[-1]

def pi_rev_check():      # Function checks which Pi Board revision we have
    # make a dictionary of known Pi board revision IDs
    rev_dict={'0002':1,'0003':1,'0004':2,'0005':2,'0006':2,'000f':2}

    # search the cpuinfo file to get the board revision ID
    revcheck = open('/proc/cpuinfo')
    cpuinfo = revcheck.readlines()
    revcheck.close()

    # put Revision ID line in a variable called matching  
    matching = [s for s in cpuinfo if "Revision" in s]

    # extract the last four useful characters containing Rev ID
    rev_num = str(matching[-1])[-5:-1] 

    # look up rev_num in our dictionary and set board_rev (-1 if not found)
    board_rev = rev_dict.get(rev_num, -1) 
    return board_rev

board_revision = pi_rev_check()
# check Pi Revision to set port 21/27 correctly
if board_revision == 1:
    # define ports list Rev 1
    ports = [25, 24, 23, 22, 21, 18, 17, 11, 10, 9, 8, 7]
else:
    # define ports list all others
    ports = [25, 24, 23, 22, 27, 18, 17, 11, 10, 9, 8, 7]


# make a copy of ports list and then reverse it as we need both directions
ports_rev = ports[:]
ports_rev.reverse()

# enable python error messages to be sent to browser window
cgitb.enable()  


# print the browser page headings
print ("Content-type:text/html\r\n\r\n")
print ("""
<html>
<head>
<title>GertBoard LED Test</title>
</head>
<body>
<h2>Hello World! Starting GertBoard Led test\n</h2>
""")
   
#export ports and set to output
commandstring = ""
for port_num in ports:
    # gpio export uses bcm port numbers
    commandstring = "gpio export " + str(port_num) + " out"
    os.system(commandstring)
    # gpio mode needs -g to use bcm port numbers
    commandstring = "gpio -g mode " + str(port_num) + " out"
    os.system(commandstring)
    
def reset_ports():
    commandstring = ""
    for port_num in ports:
        # set port to off
        # gpio write needs -g to use bcm port numbers
        commandstring = "gpio -g write " + str(port_num) + " 0"
        os.system(commandstring)
        # unexport port 
        # gpio unexport uses bcm port numbers
        commandstring = "gpio unexport " + str(port_num)
        os.system(commandstring)

def led_drive(reps, multiple, direction):       # define function to drive
    commandstring=""
    for i in range(reps):                       # repetitions, single or multiple
        for port_num in direction:              # and direction
            # gpio write needs -g to use bcm port numbers
            commandstring= "gpio -g write " + str(port_num) + " 1"
            os.system(commandstring)            # switch on an led 
            sleep(0.11)                         # wait for ~0.11 seconds
            if not multiple:                    # if we're not leaving it on
                commandstring= "gpio -g write " + str(port_num) + " 0"
                os.system(commandstring)        # switch it off again
                
print("<p>beginning test sequence</p>")

try:                                        # Call the led driver function for each test pattern
    print("<p>test sequence 1 - 3 x each port on/off singly forwards</p>")
    led_drive(3, 0, ports)
    print("<p>test sequence 2 - each port on/off singly reverse order then forwards</p>")
    led_drive(1, 0, ports_rev)
    led_drive(1, 0, ports)                  
    print("<p>test sequence 3 - each port on then off in reverse order</p>")
    led_drive(1, 0, ports_rev)
    print("<p>test sequence 4 - 2 x all port on forwards leaving on, then turn off</p>")
    led_drive(1, 1, ports)
    led_drive(1, 0, ports)        
    led_drive(1, 1, ports)
    led_drive(1, 0, ports)
except :
    reset_ports()                           # reset ports if error
    print("<p>error</p>")
reset_ports()                               # reset ports on normal exit


#print the test buttons again
print("""
<h2>Finished Test</h2>
<p>Press one of the buttons below to start the corresponding test.</p>

<table width="700" border="1">
  <tr>
    <td><div align="center">&nbsp;<a href="/cgi-bin/Ledtestv1p0p0.py"><img src="/../../LEDTestButton.png" width="155" height="89" alt="LED Test Button"/></a></div></td>
    <td><div align="center">&nbsp;<a href="/cgi-bin/Buttontestv1p0p0.py"><img src="/../../ButtonTestButton.png" width="155" height="89" alt="Button Test Button"/></a></div></td>
    <td><div align="center">&nbsp;<a href="/cgi-bin/Pottestv1p0p0.py"><img src="/../../PotTestButton.png" width="155" height="89" alt="Potentiometer Test Button"/></a> </div></td>
  </tr>
  <tr>
    <td><div align="center">&nbsp;Run LED Test Sequences</div></td>
    <td><div align="center">&nbsp;Press up to 10 buttons in 10 seconds</div></td>
    <td><div align="center">&nbsp;Potentiometer Test - either/both channels</div></td>
  </tr>
</table>

</body>
</html>
""")
