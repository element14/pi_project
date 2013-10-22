#!/usr/bin/env python

#==============================================================
#
# Authors:      Christine Smythe and Colin Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 1st November, 2013
#
# Description:  This simple Python3 program is used to check that the basic LED
#               configuration (hardware and software) is correct for the set of 4
#               PiFace boards linked to the R-Pi using a PiRack. Even if there are
#               no external LEDs the PiFace LEDs should change state as required
#               so long as the Pi-Rack and PiFace boards are correctly installed.
#               If the PiRack is not installed properly the program will not work.
#               The program allows the user to switch LEDs on and off by selecting
#               check buttons with a status panel below confirming which LEDs should
#               be ON. User can choose between:
#               a) turning all LEDs ON
#               b) turning all LEDs OFF
#               c) or using the check buttons to control individual LEDs.
#
#               This program requires Python3 otherwise the'tkinter' calls will cause
#               the code to fail.
#
# History:      Original release.
#
# Copyright:    2013 (c) Premier Farnell Limited
#
# License:      GPLv3+
#
#==============================================================

from tkinter import *
from time import sleep
import pifacedigitalio as pfio

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

class Application(Frame):
    """ GUI Application for testing LEDs. """

    def __init__(self, master):
        super(Application, self).__init__(master)  
        self.grid()
        self.master.title("LED Chooser V1.0")
        self.create_widgets()
        pfio.init(True,0,0)
        
    #.................Method: create widgets..........................
    # This creates checkbuttons
    #   - one for each of the LEDs
    #   - one to turn all LEDs ON
    #   - one to turn all LEDs OFF
    #   - one to choose individual LED control
    #
    def create_widgets(self):
        """ Create widgets for LED choices. """    

        # Set up the PiFace Board (horizontal) and LED (vertical) labels
        for board in range (1,5,1):
            Label(self,
                  text = "      Board " + str(board) + "      "
                  ).grid(row = 0, column = board, sticky = W+E+N+S)

        Label(self, text = "LED 8").grid(row = 1, column = 0, sticky = W+E+N+S)
        Label(self, text = "LED 7").grid(row = 2, column = 0, sticky = W+E+N+S)
        Label(self, text = "LED 6").grid(row = 3, column = 0, sticky = W+E+N+S)
        Label(self, text = "LED 5").grid(row = 4, column = 0, sticky = W+E+N+S)
        Label(self, text = "LED 4").grid(row = 5, column = 0, sticky = W+E+N+S)
        Label(self, text = "LED 3").grid(row = 6, column = 0, sticky = W+E+N+S)
        Label(self, text = "LED 2").grid(row = 7, column = 0, sticky = W+E+N+S)
        Label(self, text = "LED 1").grid(row = 8, column = 0, sticky = W+E+N+S)
    
        # .............create BOARD 1 check buttons...........
        self.blanktitle= " "
        self.column = 1
        buttoncolour = 'purple','red','green','red','yellow'
        # create Led 1 Board 1 check button
        self.led1board1 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led1board1,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 8, column = self.column, sticky = W+E+N+S)
        
        # create Led 2 board 1 check button
        self.led2board1 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led2board1,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 7, column = self.column, sticky = W+E+N+S)

        # create Led 3 Board 1 check button
        self.led3board1 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led3board1,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 6, column = self.column, sticky = W+E+N+S)
        
        # create Led 4 Board 1 check button
        self.led4board1 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led4board1,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 5, column = self.column, sticky = W+E+N+S)
        
        # create Led 5 board 1 check button
        self.led5board1 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led5board1,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 4, column = self.column, sticky = W+E+N+S)

        # create Led 6 Board 1 check button
        self.led6board1 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led6board1,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 3, column = self.column, sticky = W+E+N+S)

        # create Led 7 board 1 check button
        self.led7board1 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led7board1,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 2, column = self.column, sticky = W+E+N+S)

        # create Led 8 Board 1 check button
        self.led8board1 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led8board1,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 1, column = self.column, sticky = W+E+N+S)
        
   # .............create BOARD 2 check buttons...........
        self.column = 2
        # create Led 1 Board 2 check button
        self.led1board2 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led1board2,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 8, column = self.column, sticky = W+E+N+S)
        
        # create Led 2 board 2 check button
        self.led2board2 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led2board2,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 7, column = self.column, sticky = W+E+N+S)

        # create Led 3 Board 2 check button
        self.led3board2 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led3board2,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 6, column = self.column, sticky = W+E+N+S)
        
        # create Led 4 Board 2 check button
        self.led4board2 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led4board2,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 5, column = self.column, sticky = W+E+N+S)
        
        # create Led 5 board 2 check button
        self.led5board2 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led5board2,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 4, column = self.column, sticky = W+E+N+S)

        # create Led 6 Board 2 check button
        self.led6board2 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led6board2,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 3, column = self.column, sticky = W+E+N+S)

        # create Led 7 board 2 check button
        self.led7board2 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led7board2,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 2, column = self.column, sticky = W+E+N+S)

        # create Led 8 Board 2 check button
        self.led8board2 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led8board2,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 1, column = self.column, sticky = W+E+N+S)

        # .............create BOARD 3 check buttons...........
        self.column = 3
        # create Led 1 Board 3 check button
        self.led1board3 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led1board3,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 8, column = self.column, sticky = W+E+N+S)
        
        # create Led 2 board 3 check button
        self.led2board3 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led2board3,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 7, column = self.column, sticky = W+E+N+S)

        # create Led 3 Board 3 check button
        self.led3board3 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led3board3,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 6, column = self.column, sticky = W+E+N+S)
        
        # create Led 4 Board 3 check button
        self.led4board3 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led4board3,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 5, column = self.column, sticky = W+E+N+S)
        
        # create Led 5 board 3 check button
        self.led5board3 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led5board3,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 4, column = self.column, sticky = W+E+N+S)

        # create Led 6 Board 3 check button
        self.led6board3 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led6board3,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 3, column = self.column, sticky = W+E+N+S)

        # create Led 7 board 3 check button
        self.led7board3 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led7board3,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 2, column = self.column, sticky = W+E+N+S)

        # create Led 8 Board 3 check button
        self.led8board3 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led8board3,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 1, column = self.column, sticky = W+E+N+S)

        # .............create BOARD 4 check buttons...........
  
        self.column = 4
        # create Led 1 Board 4 check button
        self.led1board4 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led1board4,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 8, column = self.column, sticky = W+E+N+S)
        
        # create Led 2 Board 4 check button
        self.led2board4 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led2board4,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 7, column = self.column, sticky = W+E+N+S)

        # create Led 3 Board 4 check button
        self.led3board4 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led3board4,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 6, column = self.column, sticky = W+E+N+S)
        
        # create Led 4 Board 4 check button
        self.led4board4 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led4board4,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 5, column = self.column, sticky = W+E+N+S)
        
        # create Led 5 Board 4 check button
        self.led5board4 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led5board4,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 4, column = self.column, sticky = W+E+N+S)

        # create Led 6 Board 4 check button
        self.led6board4 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led6board4,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 3, column = self.column, sticky = W+E+N+S)

        # create Led 7 Board 4 check button
        self.led7board4 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led7board4,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 2, column = self.column, sticky = W+E+N+S)

        # create Led 8 Board 4 check button
        self.led8board4 = BooleanVar()
        Checkbutton(self,
                    text = self.blanktitle,
                    variable = self.led8board4,
                    command = self.update_text,
                    bg=buttoncolour[self.column]
                    ).grid(row = 1, column = self.column, sticky = W+E+N+S)

        # create 'All ON' button
        Button( self,
                text = "All LEDs ON",
                command = self.turnall_on,
                    bg=buttoncolour[0]
                ).grid(row=9, column = 1, sticky = W+E+N+S)
        # create 'All OFF' button
        Button( self,
                text = "All LEDs OFF",
                command = self.turnall_off,
                bg=buttoncolour[0]
                ).grid(row=9, column = 2, sticky = W+E+N+S)
        
        # create 'Use Checklist' button
        Button( self,
                text = "Use Checklist",
                command = self.update_text,
                bg=buttoncolour[0]
                ).grid(row=9, column = 3, sticky = W+E+N+S)
        
        # create text field to display results
        self.results_txt = Text(self, width = 72, height = 8, wrap = WORD)
        self.results_txt.grid(row = 11, column = 1, columnspan = 4)

    #.................... Method: turnall_on ................
    # This method turns all the LEDs on all four boards ON
    # and updates the status display to show all ON
    #
    def turnall_on(self):
        ledspacing = "....."
        status = ""
        for led in range (0,8,1):
            for board in range (0,4,1):
                pfio.digital_write(led,CLEDON,board)
                status = status + ledspacing + "LED " +str(led+1) + " ON" + ledspacing
            status = status + "\n"
        self.results_txt.delete(0.0, END)
        self.results_txt.insert(0.0, status)

    # ................. end of method: turnall_on .................
    
    #.................... Method: turnall_off ................
    # This method turns all the LEDs on all four boards OFF
    # and updates the status display to show all OFF
    #
    def turnall_off(self):
        ledOFF=".................."
        status = ""
        for led in range (0,8,1):
            for board in range (0,4,1):
                pfio.digital_write(led,CLEDOFF,board)
                status = status + ledOFF
            status = status + "\n"
        self.results_txt.delete(0.0, END)
        self.results_txt.insert(0.0, status)
        
    # ................. end of method: turnall_off .................
        
    #.................... Method: update_text ................
    # This method tests each of the LED checkbuttons to see
    # if the LED should be ON or OFF, setting the LED to the desired state
    # and updating the status display.
    #
    def update_text(self):
        """ Update text widget and display LED states. """
        status = ""
        status_allLED1=""
        status_allLED2=""
        status_allLED3=""
        status_allLED4=""
        status_allLED5=""
        status_allLED6=""
        status_allLED7=""
        status_allLED8=""
        ledOFF=".................."
        ledspacing = "....."

        # check and update for all 8 board 1 LEDs
        if self.led1board1.get():
            pfio.digital_write(CLED1,CLEDON,CBOARD1)   #turn LED on
            status_allLED1 += ledspacing + "LED 1 ON" + ledspacing
        else :
            pfio.digital_write(CLED1,CLEDOFF,CBOARD1)   #turn LED off
            status_allLED1 += ledOFF
            
        if self.led2board1.get():
            pfio.digital_write(CLED2,CLEDON,CBOARD1)   #turn LED on
            status_allLED2 += ledspacing + "LED 2 ON" + ledspacing
        else :
            pfio.digital_write(CLED2,CLEDOFF,CBOARD1)   #turn LED off
            status_allLED2 += ledOFF
            
        if self.led3board1.get():
            pfio.digital_write(CLED3,CLEDON,CBOARD1)   #turn LED on
            status_allLED3 += ledspacing + "LED 3 ON" + ledspacing
        else :
            pfio.digital_write(CLED3,CLEDOFF,CBOARD1)   #turn LED off
            status_allLED3 += ledOFF
            
        if self.led4board1.get():
            pfio.digital_write(CLED4,CLEDON,CBOARD1)   #turn LED on
            status_allLED4 += ledspacing + "LED 4 ON" + ledspacing
        else :
            pfio.digital_write(CLED4,CLEDOFF,CBOARD1)   #turn LED off
            status_allLED4 += ledOFF       

        if self.led5board1.get():
            pfio.digital_write(CLED5,CLEDON,CBOARD1)   #turn LED on
            status_allLED5 += ledspacing + "LED 5 ON" + ledspacing
        else :
            pfio.digital_write(CLED5,CLEDOFF,CBOARD1)   #turn LED off
            status_allLED5 += ledOFF

        if self.led6board1.get():
            pfio.digital_write(CLED6,CLEDON,CBOARD1)   #turn LED on
            status_allLED6 += ledspacing + "LED 6 ON" + ledspacing
        else :
            pfio.digital_write(CLED6,CLEDOFF,CBOARD1)   #turn LED off
            status_allLED6 += ledOFF
        
        if self.led7board1.get():
            pfio.digital_write(CLED7,CLEDON,CBOARD1)   #turn LED on
            status_allLED7 += ledspacing + "LED 7 ON" + ledspacing
        else :
            pfio.digital_write(CLED7,CLEDOFF,CBOARD1)   #turn LED off
            status_allLED7 += ledOFF

        if self.led8board1.get():
            pfio.digital_write(CLED8,CLEDON,CBOARD1)   #turn LED on
            status_allLED8 += ledspacing + "LED 8 ON" + ledspacing
        else :
            pfio.digital_write(CLED8,CLEDOFF,CBOARD1)   #turn LED off
            status_allLED8 += ledOFF
            
        #  check and update for all 8 board 1 LEDs
        
        if self.led1board2.get():
            pfio.digital_write(CLED1,CLEDON,CBOARD2)   #turn LED on
            status_allLED1 += ledspacing + "LED 1 ON" + ledspacing
        else :
            pfio.digital_write(CLED1,CLEDOFF,CBOARD2)   #turn LED off
            status_allLED1 += ledOFF

        if self.led2board2.get():
            pfio.digital_write(CLED2,CLEDON,CBOARD2)   #turn LED on
            status_allLED2 += ledspacing + "LED 2 ON" + ledspacing
        else :
            pfio.digital_write(CLED2,CLEDOFF,CBOARD2)   #turn LED off
            status_allLED2 += ledOFF

        if self.led3board2.get():
            pfio.digital_write(CLED3,CLEDON,CBOARD2)   #turn LED on
            status_allLED3 += ledspacing + "LED 3 ON" + ledspacing
        else :
            pfio.digital_write(CLED3,CLEDOFF,CBOARD2)   #turn LED off
            status_allLED3 += ledOFF

        if self.led4board2.get():
            pfio.digital_write(CLED4,CLEDON,CBOARD2)   #turn LED on
            status_allLED4 += ledspacing + "LED 4 ON" + ledspacing
        else :
            pfio.digital_write(CLED4,CLEDOFF,CBOARD2)   #turn LED off
            status_allLED4 += ledOFF

        if self.led5board2.get():
            pfio.digital_write(CLED5,CLEDON,CBOARD2)   #turn LED on
            status_allLED5 += ledspacing + "LED 5 ON" + ledspacing
        else :
            pfio.digital_write(CLED5,CLEDOFF,CBOARD2)   #turn LED off
            status_allLED5 += ledOFF

        if self.led6board2.get():
            pfio.digital_write(CLED6,CLEDON,CBOARD2)   #turn LED on
            status_allLED6 += ledspacing + "LED 6 ON" + ledspacing
        else :
            pfio.digital_write(CLED6,CLEDOFF,CBOARD2)   #turn LED off
            status_allLED6 += ledOFF
       
        if self.led7board2.get():
            pfio.digital_write(CLED7,CLEDON,CBOARD2)   #turn LED on
            status_allLED7 += ledspacing + "LED 7 ON" + ledspacing
        else :
            pfio.digital_write(CLED7,CLEDOFF,CBOARD2)   #turn LED off
            status_allLED7 += ledOFF

        if self.led8board2.get():
            pfio.digital_write(CLED8,CLEDON,CBOARD2)   #turn LED on
            status_allLED8 += ledspacing + "LED 8 ON" + ledspacing
        else :
            pfio.digital_write(CLED8,CLEDOFF,CBOARD2)   #turn LED off
            status_allLED8 += ledOFF
        

        #  check and update for all 8 board 3 LEDs
        
        if self.led1board3.get():
            pfio.digital_write(CLED1,CLEDON,CBOARD3)   #turn LED on
            status_allLED1 += ledspacing + "LED 1 ON" + ledspacing
        else :
            pfio.digital_write(CLED1,CLEDOFF,CBOARD3)   #turn LED off
            status_allLED1 += ledOFF

        if self.led2board3.get():
            pfio.digital_write(CLED2,CLEDON,CBOARD3)   #turn LED on
            status_allLED2 += ledspacing + "LED 2 ON" + ledspacing
        else :
            pfio.digital_write(CLED2,CLEDOFF,CBOARD3)   #turn LED off
            status_allLED2 += ledOFF

        if self.led3board3.get():
            pfio.digital_write(CLED3,CLEDON,CBOARD3)   #turn LED on
            status_allLED3 += ledspacing + "LED 3 ON" + ledspacing
        else :
            pfio.digital_write(CLED3,CLEDOFF,CBOARD3)   #turn LED off
            status_allLED3 += ledOFF

        if self.led4board3.get():
            pfio.digital_write(CLED4,CLEDON,CBOARD3)   #turn LED on
            status_allLED4 += ledspacing + "LED 4 ON" + ledspacing
        else :
            pfio.digital_write(CLED4,CLEDOFF,CBOARD3)   #turn LED off
            status_allLED4 += ledOFF

        if self.led5board3.get():
            pfio.digital_write(CLED5,CLEDON,CBOARD3)   #turn LED on
            status_allLED5 += ledspacing + "LED 5 ON" + ledspacing
        else :
            pfio.digital_write(CLED5,CLEDOFF,CBOARD3)   #turn LED off
            status_allLED5 += ledOFF

        if self.led6board3.get():
            pfio.digital_write(CLED6,CLEDON,CBOARD3)   #turn LED on
            status_allLED6 += ledspacing + "LED 6 ON" + ledspacing
        else :
            pfio.digital_write(CLED6,CLEDOFF,CBOARD3)   #turn LED off
            status_allLED6 += ledOFF
       
        if self.led7board3.get():
            pfio.digital_write(CLED7,CLEDON,CBOARD3)   #turn LED on
            status_allLED7 += ledspacing + "LED 7 ON" + ledspacing
        else :
            pfio.digital_write(CLED7,CLEDOFF,CBOARD3)   #turn LED off
            status_allLED7 += ledOFF

        if self.led8board3.get():
            pfio.digital_write(CLED8,CLEDON,CBOARD3)   #turn LED on
            status_allLED8 += ledspacing + "LED 8 ON" + ledspacing
        else :
            pfio.digital_write(CLED8,CLEDOFF,CBOARD3)   #turn LED off
            status_allLED8 += ledOFF

        #  check and update for all 8 board 4 LEDs
        
        if self.led1board4.get():
            pfio.digital_write(CLED1,CLEDON,CBOARD4)   #turn LED on
            status_allLED1 += ledspacing + "LED 1 ON" + ledspacing
        else :
            pfio.digital_write(CLED1,CLEDOFF,CBOARD4)   #turn LED off
            status_allLED1 += ledOFF

        if self.led2board4.get():
            pfio.digital_write(CLED2,CLEDON,CBOARD4)   #turn LED on
            status_allLED2 += ledspacing + "LED 2 ON" + ledspacing
        else :
            pfio.digital_write(CLED2,CLEDOFF,CBOARD4)   #turn LED off
            status_allLED2 += ledOFF

        if self.led3board4.get():
            pfio.digital_write(CLED3,CLEDON,CBOARD4)   #turn LED on
            status_allLED3 += ledspacing + "LED 3 ON" + ledspacing
        else :
            pfio.digital_write(CLED3,CLEDOFF,CBOARD4)   #turn LED off
            status_allLED3 += ledOFF

        if self.led4board4.get():
            pfio.digital_write(CLED4,CLEDON,CBOARD4)   #turn LED on
            status_allLED4 += ledspacing + "LED 4 ON" + ledspacing
        else :
            pfio.digital_write(CLED4,CLEDOFF,CBOARD4)   #turn LED off
            status_allLED4 += ledOFF

        if self.led5board4.get():
            pfio.digital_write(CLED5,CLEDON,CBOARD4)   #turn LED on
            status_allLED5 += ledspacing + "LED 5 ON" + ledspacing
        else :
            pfio.digital_write(CLED5,CLEDOFF,CBOARD4)   #turn LED off
            status_allLED5 += ledOFF

        if self.led6board4.get():
            pfio.digital_write(CLED6,CLEDON,CBOARD4)   #turn LED on
            status_allLED6 += ledspacing + "LED 6 ON" + ledspacing
        else :
            pfio.digital_write(CLED6,CLEDOFF,CBOARD4)   #turn LED off
            status_allLED6 += ledOFF
       
        if self.led7board4.get():
            pfio.digital_write(CLED7,CLEDON,CBOARD4)   #turn LED on
            status_allLED7 += ledspacing + "LED 7 ON" + ledspacing
        else :
            pfio.digital_write(CLED7,CLEDOFF,CBOARD4)   #turn LED off
            status_allLED7 += ledOFF

        if self.led8board4.get():
            pfio.digital_write(CLED8,CLEDON,CBOARD4)   #turn LED on
            status_allLED8 += ledspacing + "LED 8 ON" + ledspacing
        else :
            pfio.digital_write(CLED8,CLEDOFF,CBOARD4)   #turn LED off
            status_allLED8 += ledOFF

        # Finally update the status display for all LEDs on all boards
        status = status + status_allLED1 + "\n" + status_allLED2 + "\n"
        status = status + status_allLED3 + "\n" + status_allLED4 + "\n"
        status = status + status_allLED5 + "\n" + status_allLED6 + "\n"
        status = status + status_allLED7 + "\n" + status_allLED8 + "\n"
        self.results_txt.delete(0.0, END)
        self.results_txt.insert(0.0, status)

        # end of method: update_text..............................

#=================================================================
# main
#=================================================================

root = Tk()                             # Create the GUI root object
root.title("LED Chooser")
app = Application(root)                 # Create the root application window
root.mainloop()
