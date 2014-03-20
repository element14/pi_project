#!/usr/bin/env python2.7

#==============================================================
#
# Authors:      Christine Smythe and Jenny Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 21st February 2014
#
# Description:  This Python program is designed to be called from a browser.
#               It is an adaptation of the program atod.py by Alex Eames of http://RasPi.TV 
#               who based his on the button test by Gert Jan van Loo & Myra VanInwegen.
#               It reports up to 10 button presses/releases for up to 10 seconds
#               This programs structure:
#                   exports the button GPIO pins and sets to mode 'up'
#                   (so pin will read 0 when button pressed and 1 when not)
#                   prints the browser page headings
#                   for up to 100 iterations or until 10 button state changes
#                       reads all 3 current button states
#                       checks to see if any button state has changed
#                           if changed
#                               prints "button pressed" or "button released" as appropriate
#                   if no button presses detected
#                       prints "No button presses detected"
#                   resets the button ports by unexporting them
#                   prints the test buttons
#
# History:      Original release.
#
# Copyright:    2014 (c) Premier Farnell Limited
#
# License:      GPLv3+
#
#==============================================================

import cgi
import cgitb
from time import sleep
import sys
import os
import subprocess

# enable python error messages to be sent to browser window
cgitb.enable()  
print ("Content-type:text/html\r\n\r\n")
print ("""
<html>
<head>
<title>GertBoard Button Test</title>
</head>
<body>
<h2>Starting GertBoard Button test\n</h2>
""")

# export ports 23 24 and 25 so we can access them and set to input/pullup
# 'gpio export' uses  BCM_GPIO pin numbers
commandstring = ""
for port_num in range(23,26):
    result=0
    stderr = 0
    commandstring = "gpio export " + str(port_num) + " in"
    result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
    result=0
    stderr = 0
    # !!!! must us -g flag in 'gpio mode' call to use BCM_GPIO pin numbers!!!!
    commandstring = "gpio -g mode " + str(port_num) + " up"
    result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
print("<p>Button ports initialised</p>")
    
#.................... Method: reset_ports ................
# This method unexports button pins BCM 23,24,25
# Note that 'gpio unexport' uses  BCM_GPIO pin numbers
#
def reset_ports():                              # resets the ports for a safe exit
    for port_num in range(23,26):
        result=0
        stderr = 0
        commandstring = "gpio unexport " + str(port_num)
        result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
    print("Button ports reset</p>")
#...............................end of method: reset_ports...................


#.................... Method: digitalRead ................
# This method uses gpio read to get the current state of a pin
# must use -g flag in 'gpio read' to use BCM_GPIO pin numbers!!!!
#
#
def digitalRead(pin):
    result=0
    stderr = 0
    #first setup the command string
    commandstring = "gpio -g read " + str(pin)
    #then pass it to subprocess to execute
    result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
    # gpio read will return a string  - either "0/n" or "1/n"
    # so just return the first character "0" or "1"
    return result[0]
#...............................end of method: digitalRead ...................

#now loop while waiting for button presses and print when a button changes
current_status=0
loopcount = 0
button_press = 0                            # set intial values for variables
status_list = [1,1,1]
previous_status = [1,1,1]
while button_press < 10 and loopcount <100:    # read inputs constantly until 10 changes made or 100 loops
    #get current state of buttons
    status_list = [digitalRead(25), digitalRead(24), digitalRead(23)]
    print("<p>")
    # check each button to see if it has changed
    for i in range (0,3):
        if status_list[i]== "0" and previous_status [i]=="1":
            print ("button " +str(i) + " pressed ")
            button_press += 1
        elif status_list[i]== "1" and previous_status [i]=="0":
            print ("button " +str(i) + " released ")
    print("</p>")
    loopcount += 1
    previous_status = status_list
if button_press ==0:
    print("<p>No button presses detected</p>")
# finish by unexporting the ports
reset_ports()

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

