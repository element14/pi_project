#!/usr/bin/env python

#==============================================================
#
# Authors:      Colin Smythe and Christine Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 1st November, 2013
#
#Description:   This simple Python3 program is used to check that the external
#               and onboard (to the PiFace boards) switches are correctly configured.
#               the sequence of tests is:");
#               1) A request will be made to press each of the onboard switches;
#               2) A request will be made to press each of the external switches.
#
#               If you do not press the switch OR the PiFace Digital board is not");
#               present then the test will proceed to the next switch.  One of three");
#               reports will be printed:");
#               1) The button was pressed;");
#               2) A timeout occurred;");
#               3) No PiFace Digital Board is not present.").
#
#               The code shows how to construct the wait until a switch is pressed OR
#               until a predefined timeout period has expired.
#
# History:      Original release.
#
# Copyright:    2013 (c) Premier Farnell Limited
#
# License:      GPLv3+
#
#==============================================================

import pifacedigitalio as pfio;
from time import sleep;

pfio.init(True,0,0);    # Assumes the PiRack SPI CE jumpers are in the unswapped position.
                        # If the PiRack SPI CE jumpers are in the swapped position use:
                        # pfio.init(True,0,1);

#==============================================================
# Declaration of Constants

CSWITCHOFF = 0;         # Switch LED off
CSWITCHON = 1;          # Switch LED on

CBOARD1 = 0;            # PiFace board 0
CBOARD2 = 1;            # PiFace board 1
CBOARD3 = 2;            # PiFace board 2
CBOARD4 = 3;            # PiFace board 3

CSWITCHSTART = 0;       # Switch Start
CSWITCHCOL1 = 1;        # Switch for Column 1
CSWITCHCOL2 = 2;        # Switch for Column 2
CSWITCHCOL3 = 3;        # Switch for Column 3
CSWITCHCOL4 = 4;        # Switch for Column 4
CSWITCHSTOP = 5;        # Switch for Column 5

CSWITCHBOARDSTART = 0;  # Switch Start
CSWITCHBOARDCOL1 = 0;   # Switch for Column 1
CSWITCHBOARDCOL2 = 0;   # Switch for Column 2
CSWITCHBOARDCOL3 = 0;   # Switch for Column 3
CSWITCHBOARDCOL4 = 0;   # Switch for Column 4
CSWITCHBOARDSTOP = 0;   # Switch for Column 5

CMAXCOUNT = 1500;       # Switch timeout period count maximum

#==============================================================
# Print the test header information

print ("PiFace Configuration SWITCH Test");
print ("================================");
print ("");
print ("Authors:      Colin Smythe and Christine Smythe (Dunelm Services Limited");
print ("Version:      1.0");
print ("Release Date: 1st November, 2013");
print ("");
print ("Description:  This simple Python3 program is used to check that the external");
print ("              and onboard (to the PiFace boards) switches are correctly configured.");
print ("              The sequence of tests is:");
print ("              1) A request will be made to press each of the onboard switches;");
print ("              2) A request will be made to press each of the external switches.");
print ("");
print ("              If you do not press the switch OR the PiFace Digital board is not");
print ("              present then the test will proceed to the next switch.  One of three");
print ("              reports will be printed:");
print ("              1) The button was pressed;");
print ("              2) A timeout occurred;");
print ("              3) No PiFace Digital Board is not present.");
print ("");
print ("-----------------------------");
print ("");

#==============================================================
# Test all of the available PiFace Onboard Switches

print ("PiFace Digital ONBOARD Switch Test Start");
print ("");
print ("You will be asked to press each of the on-board switches (4 per PiFace Digital).");
print ("If you do not press the switch OR the PiFace Digital board is not present then");
print ("the test will proceed to the next switch.  One of three reports will be printed:");
print ("1) The button was pressed;");
print ("2) A timeout occurred;");
print ("3) No PiFace Digital Board is not present.");


for loopBoard in range (0,4,1):
    for loopSwitch in range (0,4,1):
        count = 0;
        print("");
        print ("Press Onboard Button " + str(loopSwitch) + " on PiFace Board " + str(loopBoard));
        input_value = pfio.digital_read (loopSwitch, loopBoard);
        if input_value == False:
            while input_value == False and count < CMAXCOUNT:
                input_value = pfio.digital_read (loopSwitch, loopBoard);
                count = count + 1;
        
        if count == 0:
            print ("No PiFace Digital Board")
        elif count < CMAXCOUNT:
            print ("Button Pressed");
        else:
            print ("*** TIMEOUT");

print ("");
print ("Individual Onboard Switch Tests Complete");
print ("");

#==============================================================
# Test all of the available external Switches

print ("PiFace Digital EXTERNAL Switch Test Start");
print ("");
print ("You will be asked to press each of the external switches (6 on PiFace Digital board 0).");
print ("If you do not press the switch OR the PiFace Digital board is not present then");
print ("the test will proceed to the next switch.  One of three reports will be printed:");
print ("1) The button was pressed;");
print ("2) A timeout occurred;");
print ("3) No PiFace Digital Board is not present.");

#==============================================================
# Test the external switch 'Start'

count = 0;
print("");
print ("Press External button 'Start' on PiFace Digital board 0");
input_value = pfio.digital_read (CSWITCHSTART, CSWITCHBOARDSTART);
if input_value == False:
    while input_value == False and count < CMAXCOUNT:
        input_value = pfio.digital_read (CSWITCHSTART, CSWITCHBOARDSTART);
        count = count + 1;
        
    if count == 0:
        print ("No PiFace Digital Board")
    elif count < CMAXCOUNT:
        print ("Start Button Pressed");
    else:
        print ("*** TIMEOUT");

#==============================================================
# Test the external switch 'Switch 1'

count = 0;
print("");
print ("Press External button 'Switch 1' on PiFace Digital board 0");
input_value = pfio.digital_read (CSWITCHCOL1, CSWITCHBOARDCOL1);
if input_value == False:
    while input_value == False and count < CMAXCOUNT:
        input_value = pfio.digital_read (CSWITCHCOL1, CSWITCHBOARDCOL1);
        count = count + 1;
        
    if count == 0:
        print ("No PiFace Digital Board")
    elif count < CMAXCOUNT:
        print ("Switch 1 Button Pressed");
    else:
        print ("*** TIMEOUT");

#==============================================================
# Test the external switch 'Switch 2'

count = 0;
print("");
print ("Press External button 'Switch 2' on PiFace Digital board 0");
input_value = pfio.digital_read (CSWITCHCOL2, CSWITCHBOARDCOL2);
if input_value == False:
    while input_value == False and count < CMAXCOUNT:
        input_value = pfio.digital_read (CSWITCHCOL2, CSWITCHBOARDCOL2);
        count = count + 1;
        
    if count == 0:
        print ("No PiFace Digital Board")
    elif count < CMAXCOUNT:
        print ("Switch 2 Button Pressed");
    else:
        print ("*** TIMEOUT");

#==============================================================
# Test the external switch 'Switch 3'

count = 0;
print("");
print ("Press External button 'Switch 3' on PiFace Digital board 0");
input_value = pfio.digital_read (CSWITCHCOL3, CSWITCHBOARDCOL3);
if input_value == False:
    while input_value == False and count < CMAXCOUNT:
        input_value = pfio.digital_read (CSWITCHCOL3, CSWITCHBOARDCOL3);
        count = count + 1;
        
    if count == 0:
        print ("No PiFace Digital Board")
    elif count < CMAXCOUNT:
        print ("Switch 3 Button Pressed");
    else:
        print ("*** TIMEOUT");

#==============================================================
# Test the external switch 'Switch 4'

count = 0;
print("");
print ("Press External button 'Switch 4' on PiFace Digital board 0");
input_value = pfio.digital_read (CSWITCHCOL4, CSWITCHBOARDCOL4);
if input_value == False:
    while input_value == False and count < CMAXCOUNT:
        input_value = pfio.digital_read (CSWITCHCOL4, CSWITCHBOARDCOL4);
        count = count + 1;
        
    if count == 0:
        print ("No PiFace Digital Board")
    elif count < CMAXCOUNT:
        print ("Swicth 4 Button Pressed");
    else:
        print ("*** TIMEOUT");

#==============================================================
# Test the external switch 'Stop'

count = 0;
print("");
print ("Press External button 'Stop' on PiFace Digital board 0");
input_value = pfio.digital_read (CSWITCHSTOP, CSWITCHBOARDSTOP);
if input_value == False:
    while input_value == False and count < CMAXCOUNT:
        input_value = pfio.digital_read (CSWITCHSTOP, CSWITCHBOARDSTOP);
        count = count + 1;
        
    if count == 0:
        print ("No PiFace Digital Board")
    elif count < CMAXCOUNT:
        print ("Stop Button Pressed");
    else:
        print ("*** TIMEOUT");

#==============================================================

print ("");
print ("Individual External Switch Tests Complete");
print ("");

pfio.deinit();

print ("=============================");
print ("");
print ("Completion of all tests");
print ("");
print ("=============================");
print ("");

