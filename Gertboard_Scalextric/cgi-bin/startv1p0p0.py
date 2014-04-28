#!/usr/bin/python2.7

#==============================================================
#
# Author:       Christine Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 28th April 2014
#
# Description:  This Python program is designed to be called from a browser.
#               It is used to start the car.  The value of the pwm is set to '250'.
#
# History:      Original release.
#
# Copyright:    2014 (c) Premier Farnell Limited
#
# License:      GPLv3+
#
#==============================================================

from __future__ import print_function       
from time import sleep
                        
#import wiringpi
import termios
import tty
import sys          # so we can get the board type/revision
import os           # so we can make gpio calls export, unexport and write
import subprocess
# import cgi and cgitb to enable python error messages to be sent to browser window
import cgi
import cgitb
cgitb.enable()

board_type = sys.argv[-1]

def start_browserpage():
    print ("Content-type:text/html; charset=UTF-8")
    print("""
    <html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Gertboard Scalextric Car Controller Program</title>
    <meta name="language" content="en-US" />
    <meta name="author" content="Jennifer Smythe (Dunelm Services) and Colin Smythe (Dunelm Services)" />
    <meta name="date" content="16th April 2014" />
    <meta name="status" content="Final" />
    <meta name="version" content="1.0.0" />
    <meta name="publisher" content="Premier Farnell" />
    <meta name="history" content="The first release." />
    <style type="text/css">
      h1 {
	         font-size: 36px;
	         font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
          }          
    </style>
  </head> 
  <body>
    <h1 align="center">Scalextric Controller Program</h1>
    <hr/>
        <table width="450" border="0" align="center" bgcolor="#CCC">   
      <tr>
        <td></td>
        <td><div align="center"><p><a href="/cgi-bin/startv1p0p0.py"><img src="/../../StartButtonv1p0p0.png" width="120" height="75" alt="Start Button"/></a></p></div></td>
        <td></td>
      </tr>
      <tr>
        <td><div align="center"><a href="/cgi-bin/slowerv1p0p0.py"><img src="/../../SlowerButtonv1p0p0.png" width="120" height="75" alt="Slower Button"/></a></div></td>
        <td bgcolor="#FFF"><div align="center">
""")
          
#   pwm_value = the PWM value to be displayed 
def add_pwm_to_browserpage(pwm_value):
    print( "<p><b>Speed</b><br/>")
    print ("{0:04d}".format(pwm_value))
    print ("</p>") 
#<p><b>Speed</b><br/>0</p>

def end_browserpage():
    print("""
    </div></td>
    <td><div align="center"><a href="/cgi-bin/fasterv1p0p0.py"><img src="/../../FasterButtonv1p0p0.png" width="120" height="75" alt="Faster Button"/></a></div></td>
      </tr>
      <tr>
        <td></td>
        <td><div align="center"><p><a href="/cgi-bin/stopv1p0p0.py"><img src="/../../StopButtonv1p0p0.png" width="120" height="75" alt="Stop Button"/></a></p></div></td>
        <td></td>
      </tr>
    </table>
    
    <div align="center"><p>To control your Scalextric Car use the buttons above.</p></div>
    
    <hr/>
    </body>
    </html>
    """)  




def store_pwmvalue(newpwm):
    # store the new pwm value
    pwmfile= open("pwmvalue.txt",'w')
    pwmfile.write(str(newpwm))
    pwmfile.close()


# Set up the GPIO system to drive the motor using PWM
# Note we are using GPIO.BCM pin numbering
def setup_ports():
    #export ports and set to output
    commandstring = ""
    result=0
    stderr = 0
    # gpio export uses bcm port numbers
    commandstring = "gpio export 17 out"
    result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
    commandstring = "gpio export 18 out"
    result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
    #gpio mode needs -g to use bcm port numbers
    commandstring = "gpio -g mode 17 out"
    result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
    commandstring = "gpio -g mode 18 pwm"
    result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
    commandstring = "gpio -g write 17 0"
    result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
    commandstring = "gpio -g pwm 18 0"
    result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)


def close_ports():
    commandstring = ""
    result=0
    stderr = 0
    # gpio export uses bcm port numbers
    commandstring = "gpio unexport 17"
    result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
    commandstring = "gpio unexport 18"
    result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)

# define constants and variables used
char = '#'                  # define the bar chart character 
pwm_start_value = 250
commandstring = ""
result=0
stderr = 0

# ****************   main code starts here   ****************************
setup_ports()

commandstring = "gpio -g pwm 18 " + str(pwm_start_value)
result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
store_pwmvalue(pwm_start_value)                # store the pwm in the file pwmvalue.txt
start_browserpage()                             # print the start of the Browser page
add_pwm_to_browserpage(pwm_start_value)                   # add the PWM display bar
end_browserpage()                               # end the browser page
