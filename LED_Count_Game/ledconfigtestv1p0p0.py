#!/usr/bin/env python

#==============================================================
#
# Authors:      Colin Smythe and Christine Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 1st November, 2013
#
# Description:  This simple Python3 program is used to check that the basic LED
#               configuration (hardware and software) is correct for the 4 set of
#               PiFace boards linked to the R-Pi using a PiRack. Even if there are
#               no external LEDs the PiFace LEDs should change state as required.
#               When watching the LEDs the following should be observed:
#               1) All LEDs should be off
#               2) The individual LEDs connected to PiFace 0 will switch on, and then off
#               3) As per the 2) above repeated for PiFace boards 1, 2 and 3 in sequence
#               4) All LEDs are now off
#               5) All LEDs on PiFace 0 are switched on together for 3 secs and then switched off
#               6) As per 5) above repeated for PiFace boards 1, 2, and 3 in sequence
#               7) All LEDs should be off
#               8) All LEDs on ALL PiFace boards are switched on together for 5 sec and then switched off
#               9) All LEDs should be off
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

CLEDOFF = 0;            # Switch LED off
CLEDON = 1;             # Switch LED on

CBOARD1 = 0;            # PiFace board 0
CBOARD2 = 1;            # PiFace board 1
CBOARD3 = 2;            # PiFace board 2
CBOARD4 = 3;            # PiFace board 3

CLED1 = 0;              # LED 0
CLED2 = 1;              # LED 1
CLED3 = 2;              # LED 2
CLED4 = 3;              # LED 3
CLED5 = 4;              # LED 4
CLED6 = 5;              # LED 5
CLED7 = 6;              # LED 6
CLED8 = 7;              # LED 7

#==============================================================
# Print the test header information

print ("PiFace Configuration LED Test");
print ("=============================");
print ("");
print ("Authors:      Colin Smythe and Christine Smythe (Dunelm Services Limited");
print ("Version:      1.0");
print ("Release Date: 1st November, 2013");
print ("");
print ("Description:  This simple Python3 program is used to check that the basic LED");
print ("              configuration (hardware and software) is correct for the 4 set of");
print ("              PiFace boards linked to the R-Pi using a PiRack. Even if there are");
print ("              no external LEDs the PiFace LEDs should change state as required.");
print ("              When watching the LEDs the following should be observed:");
print ("              1) All LEDs should be off");
print ("              2) The individual LEDs connected to PiFace 0 will switch on, and then off");
print ("              3) As per the 2) above repeated for PiFace boards 1, 2 and 3 in sequence");
print ("              4) All LEDs are now off");
print ("              5) All LEDs on PiFace 0 are switched on together for 3 secs and then switched off");
print ("              6) As per 5) above repeated for PiFace boards 1, 2, and 3 in sequence");
print ("              7) All LEDs should be off");
print ("              8) All LEDs on ALL PiFace boards are switched on together for 5 sec and then switched off together");
print ("              9) All LEDs should be off");
print ("");
print ("-----------------------------");
print ("");

#==============================================================
# Switch all LEDs off

for loopBoard in range (0,4,1):
    for loopLed in range (0,8,1):
        pfio.digital_write (loopLed, CLEDOFF, loopBoard);

#==============================================================
# Individual LED test

print ("Individual LED Test Start");
print ("When watching the LEDs the following should be observed:");
print ("1) All LEDs should be off");
print ("2) The individual LEDs connected to PiFace 0 will switch on, and then off");
print ("3) As per above repeated for PiFace boards 1, 2 and 3 in sequence");

for loopBoard in range (0,4,1):
    for loopLed in range (0,8,1):
        pfio.digital_write (loopLed, CLEDON, loopBoard);
        sleep (0.5);
        pfio.digital_write (loopLed, CLEDOFF, loopBoard);

print ("Individual LED Test Complete");
print ("");

#==============================================================
# Full board 0 LED test

print ("Full Board 0 LED Test Start");
print ("When watching the LEDs the following should be observed:");
print ("1) All LEDs should be off");
print ("2) All LEDs on PiFace 0 are switched on together for 3 secs and then switched off");

pfio.digital_write(CLED1,CLEDON,CBOARD1);
pfio.digital_write(CLED2,CLEDON,CBOARD1);
pfio.digital_write(CLED3,CLEDON,CBOARD1);
pfio.digital_write(CLED4,CLEDON,CBOARD1);
pfio.digital_write(CLED5,CLEDON,CBOARD1);
pfio.digital_write(CLED6,CLEDON,CBOARD1);
pfio.digital_write(CLED7,CLEDON,CBOARD1);
pfio.digital_write(CLED8,CLEDON,CBOARD1);

sleep(3);

for loopLed in range (0,8,1):
    pfio.digital_write (loopLed, CLEDOFF, CBOARD1);

print ("Full Board 0 LED Test Complete");
print ("");

#==============================================================
# Full board 1 LED test

print ("Full Board 1 LED Test Start");
print ("1) All LEDs should be off");
print ("2) All LEDs on PiFace 1 are switched on together for 3 secs and then switched off");

pfio.digital_write(CLED1,CLEDON,CBOARD2);
pfio.digital_write(CLED2,CLEDON,CBOARD2);
pfio.digital_write(CLED3,CLEDON,CBOARD2);
pfio.digital_write(CLED4,CLEDON,CBOARD2);
pfio.digital_write(CLED5,CLEDON,CBOARD2);
pfio.digital_write(CLED6,CLEDON,CBOARD2);
pfio.digital_write(CLED7,CLEDON,CBOARD2);
pfio.digital_write(CLED8,CLEDON,CBOARD2);

sleep(3);

for loopLed in range (0,8,1):
    pfio.digital_write (loopLed, CLEDOFF, CBOARD2);

print ("Full Board 1 LED Test Complete");
print ("");

#==============================================================
# Full board 2 LED test

print ("Full Board 2 LED Test Start");
print ("1) All LEDs should be off");
print ("2) All LEDs on PiFace 2 are switched on together for 3 secs and then switched off");

pfio.digital_write(CLED1,CLEDON,CBOARD3);
pfio.digital_write(CLED2,CLEDON,CBOARD3);
pfio.digital_write(CLED3,CLEDON,CBOARD3);
pfio.digital_write(CLED4,CLEDON,CBOARD3);
pfio.digital_write(CLED5,CLEDON,CBOARD3);
pfio.digital_write(CLED6,CLEDON,CBOARD3);
pfio.digital_write(CLED7,CLEDON,CBOARD3);
pfio.digital_write(CLED8,CLEDON,CBOARD3);

sleep(3);

for loopLed in range (0,8,1):
    pfio.digital_write (loopLed, CLEDOFF, CBOARD3);

print ("Full Board 2 LED Test Complete");
print ("");

#==============================================================
# Full board 3 LED test

print ("Full Board 3 LED Test Start");
print ("1) All LEDs should be off");
print ("2) All LEDs on PiFace 3 are switched on together for 3 secs and then switched off");

pfio.digital_write(CLED1,CLEDON,CBOARD4);
pfio.digital_write(CLED2,CLEDON,CBOARD4);
pfio.digital_write(CLED3,CLEDON,CBOARD4);
pfio.digital_write(CLED4,CLEDON,CBOARD4);
pfio.digital_write(CLED5,CLEDON,CBOARD4);
pfio.digital_write(CLED6,CLEDON,CBOARD4);
pfio.digital_write(CLED7,CLEDON,CBOARD4);
pfio.digital_write(CLED8,CLEDON,CBOARD4);

sleep(3);

for loopLed in range (0,8,1):
    pfio.digital_write (loopLed, CLEDOFF, CBOARD4);

print ("Full Board 3 LED Test Complete");
print ("");

#==============================================================
# Full board set test

print ("Full Board Set LED Test Start");
print ("1) All LEDs should be off");
print ("2) All LEDs on ALL PiFace boards are switched on together for 5 secs and then switched off together");

for loopBoard in range (0,4,1):
    for loopLed in range (0,8,1):
        pfio.digital_write (loopLed, CLEDON, loopBoard);

sleep (5);

print ("Full Board Set LED Test Complete");

#==============================================================
# Switch all LEDs off

for loopBoard in range (0,4,1):
    for loopLed in range (0,8,1):
        pfio.digital_write (loopLed, CLEDOFF, loopBoard);

#==============================================================

pfio.deinit();

print ("");
print ("Completion of all tests");
print ("");
print ("=============================");
print ("");






