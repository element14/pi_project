#!/usr/bin/env python2.7

#==============================================================
#
# Authors:      Christine Smythe and Jenny Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 21st February 2014
#
# Description:  This Python program is designed to be called from a browser.
#               It is an adaptation of the program atod.py by Alex Eames of http://RasPi.TV 
#               who based his on the atod test by Gert Jan van Loo & Myra VanInwegen.
#               It reads the Potentiometer values on both channels every 0.05 secs  for 5 seconds
#               and prints the results as both values and a bar representation.
#               This programs structure:
#                   exports the AtoD GPIO pins
#                   loads the SPI
#                   initialises the SPI
#                   prints the browser page headings
#                   iteratively
#                       reads both AtoD channels
#                       prints values and display bar
#                   prints the test buttons
#
# History:      Original release.
#
# Copyright:    2014 (c) Premier Farnell Limited
#
# License:      GPLv3+
#
#==============================================================

# import Python 3 print function to prevent line breaks. All prints need ()
from __future__ import print_function       
from time import sleep

# import subprocess so we can make gpio calls export, unexport and load spi
import subprocess

# import spidev so we can use xfer2 to read SPI channels
import spidev

# import cgi and cgitb to enable python error messages to be sent to browser window
import cgi
import cgitb
cgitb.enable()

#.................... Method: get_adc ................
# This method gets the current AtoD value on the requested channel
# and returns the value which will be in the range 0 to 1023
# Note that channel must be either 0 or 1
#
# EXPLANATION of 
# r = spi.xfer2([1,(2+channel)<<6,0])
# Send start bit, sgl/diff, odd/sign, MSBF 
# channel = 0 sends 0000 0001 1000 0000 0000 0000
# channel = 1 sends 0000 0001 1100 0000 0000 0000
# sgl/diff = 1; odd/sign = channel; MSBF = 0 

# EXPLANATION of 
# ret = ((r[1]&15) << 6) + (r[2] >> 2)
# spi.xfer2 returns same number of 8-bit bytes as sent. In this case, three 8-bit bytes are returned
# We must then parse out the correct 10-bit byte from the 24 bits returned. The following line discards
# To explain in even more detail....
# So with ret being 16 bit : logical 'and' the contents of byte 1 with 15(=00001111) to get those bottom 4 bits
# giving 0000 0000 0000 DDDD which we then move 6 bits left (<<6) to give 0000 00DD DD00 0000
# which makes space for the bits we need from byte 2 (the Ds in DDDD DDXX) 
# then take byte 2 (DDDD DDXX) , move 2 bits right (>>2) to get 00DD DDDD
# then add the two (00DD DDDD to 0000 00DD DD00 0000) to give 0000 00DD DDDD DDDD
# NB this differs from original atod.py program which used 31 as the logical 'and' to get bottom 4 bits
# but I believe using 31 (00011111) gives bottom 5 bits whereas using 15 (00001111) gives the correct 4 bits.
# The original atod.py program will still work providing the extra bit is 0, which it has been in all my tests.
# Such a lot of explanation for such a little amount of code!!!

def get_adc(channel):                           # read SPI data from MCP3002 chip
    if ((channel > 1) or (channel < 0)):        # Only 2 channels 0 and 1 else return -1
        return -1
    r = spi.xfer2([1,(2+channel)<<6,0]) 
    ret = ((r[1]&15) << 6) + (r[2] >> 2)
    return ret 

#.................... Method: reset_spi_ports ................
# This method unexports ports BCM 28,29,30,31 (GPIO 8,9,10,11)
# Note that 'gpio unexport' uses  BCM_GPIO pin numbers
#
def reset_spi_ports():      # resets the ports for a safe exit
    for port_num in range(28,32):
        result=0
        stderr = 0
        commandstring = "gpio unexport " + str(port_num)
        result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
    print("AtoD ports reset</p>")

#.................... Method: init_spi_ports ................
# This method exports AtoD ports BCM 28,29,30,31 (GPIO 8,9,10,11) as input
# so that non-root browser users can access them
# Note that 'gpio unexport' uses  BCM_GPIO pin numbers
# It then loads the SPI module
#
def init_spi_ports():
    commandstring = ""
    # first export the ports
    for port_num in range(28,32):
        result=0
        stderr = 0
        commandstring = "gpio export " + str(port_num) + " in"
        result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
    # now load spi module
        result=0
        stderr = 0
        commandstring = "gpio load spi"
        result = subprocess.check_output(commandstring, shell=True, stderr=subprocess.STDOUT)
    print("<p>AtoD ports initialised</p>")
# ........................ end of Method init_spi_ports .........................

# Main code section starts here....


# print the header for the browser page
print ("Content-type:text/html\r\n\r\n")
print ("""
<html>
<head>
<title>GertBoard Potentiometer Test</title>
</head>
<body>
<h2>Starting GertBoard Potentiometer test\n</h2>
""")

# initialise the spi ports and spidev software
init_spi_ports()
spi = spidev.SpiDev()
spi.open(0,0)               # The Gertboard ADC is on SPI channel 0 (CE0 - aka GPIO8)

iterations = 0              # initial value for iteration counter
char = '#'                  # define the display bar character
channel_0 = 0
channel_1 = 1

# Now read both channels and construct the display bar
# Max atod value is 1023 so display bar will show 1 "#" character for every 24 ( max 42)
# These values are chosen to fit on an ipad screen in landscape mode
print("<p>Channel 0 ............................................................................")
print(".............................................................................Channel 1</p>")
while iterations < 100:
    adc_value_0 = (get_adc(channel_0))
    adc_value_1 = (get_adc(channel_1))
    reps = adc_value_0 / 24
    spaces = 42 - reps
    bar_string = "  " + reps * char + spaces * "_"
    reps = adc_value_1 / 24
    spaces = 42 - reps
    bar_string = bar_string + "\t" + spaces * "_" + reps * char + "  "
    print("<p>" + "{0:04d}".format(adc_value_0) + bar_string + "{0:04d}".format(adc_value_1) + "</p>")
    sleep(0.05)       # wait before reading again
    iterations += 1   # limits length of program running to approx 5s [100 * 0.05]


# reset spi ports before exiting
reset_spi_ports()


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


