#!/usr/bin/env python

#==============================================================
#
# Authors:      Christine Smythe and Colin Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 1st November, 2013
#
# Description:  This Python3 program runs the LED Counting Game
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
import random

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

CMAXCONFIGS = 255;      # The maximum number of configurations
CDEFAULTCONFIGS = 10;   # The default number of configurations
CDEFAULTSPEED = 5000;   # default game speed set to maximum of 5000 = 5 seconds

CSTARTBUTTON = 0;       # start button is button 0 on board 0
CLEDCOL1_BUTTON = 1;    # button to choose LED column 1
CLEDCOL2_BUTTON = 2;    # button to choose LED column 2
CLEDCOL3_BUTTON = 3;    # button to choose LED column 3
CLEDCOL4_BUTTON = 4;    # button to choose LED column 4
CSTOPBUTTON = 5;        # Stop button is button 5 on board 0
CBOARDwithBUTTONS = 0;  # the piface with the buttons wired is board 0
CSTR_LEDON = "ON";
CSTR_LEDOFF = "OFF";

# constants for accessing elements of player results table
C_correct_column =0;
C_player_answer =1;
C_player_correct = 2;
C_player_time = 3;

#constants for putting text on correct line in choices panel
CCONFIGS_ROW = 0.0;
CSPEED_ROW = 2.0;
CREADYTOSTART_ROW = 4.0;
CSTARTED_ROW = 6.0;
CSTOPPED_ROW = 7.0;
CFINISHED_ROW = 7.0;




CINSTRUCTIONS = """How to play the LED Counting Game: 
1. Choose how many configurations you want to play 1 to 255.
2. Choose how quickly you have to choose the right one - from 200ms up to 5000ms ( 0.2 seconds to 5 seconds).
3. Press start to initialise the game.
4. The LEDs on the game board will flash in a quadrant pattern until you press the start button on the game board.
5. You then have to choose which column has the most LEDs lit and press the game button for that column.
6. When you have finished the results will be displayed on the screen.
Good Luck!
"""

#==============================================================

class Application(Frame):
    """ GUI Application for LED Counting Game. """

    def __init__(self, master):
        super(Application, self).__init__(master)  
        self.grid()
        self.master.title("LED Counting Game V1.0")
        # initialise the GUI window ready for user interaction
        self.create_widgets()
        # initialise the PiFace digital i/o package
        # so we can control the boards and hence the LEDs
        pfio.init(True,0,0)
        
    #.................Method: create widgets..........................
    # This creates the GUI by setting up ....
    #   - the instructions
    #   - the text and entry for the player to enter game speed
    #   - the text and entry for the player to enter number of configurations
    #   - SETUP checkbutton
    #   - START checkbutton
    #   - the text area for game choices
    #   - the text area for results
    #   - the text area for statistics
    #   - the data table to store the player results
    #
    def create_widgets(self):
        """ Create widgets for LED choices. """    
     
        # setup the instruction label
        Label(self, text = CINSTRUCTIONS).grid(row = 0, column = 0, rowspan = 1, columnspan = 3)
        
        # setup the widgets to get the number of configurations
        Label(self, text = "Enter Number of Configurations 1 to 255:").grid(row = 2,
                                                                    column = 0)
        self.configs_ent = Entry(self)
        self.configs_ent.grid(row = 3, column = 0)


        # setup the widgets to get the time interval
        Label(self, text = "Enter speed 200 to 5000 ms : ").grid(row = 4,
                                                        column = 0)
        self.speed_ent = Entry(self)
        self.speed_ent.grid(row = 5, column = 0) 

        # create 'SETUP GAME' button
        Button( self,
                text = "SETUP GAME",
                command = self.choose_game_setup,
                    bg='yellow'
                ).grid(row=6, column = 0, sticky = W+E+N+S)      
       
        # create 'START GAME' button
        Button( self,
                text = "START GAME",
                command = self.start_game,
                    bg='green'
                ).grid(row=7, column = 0, sticky = W+E+N+S)
        
      # create text field to display the choices
        self.choices_txt = Text(self, width = 45, height = 7, wrap = WORD)
        self.choices_txt.grid(row = 9, column = 0, columnspan = 1)
        # create text field to display the statistics
        self.stats_txt = Text(self, width = 45, height = 8, wrap = WORD)
        self.stats_txt.grid(row = 10, column = 0, columnspan = 1)
        # create text field to display the results
        self.results_txt = Text(self, width = 55, height = 25, wrap = WORD)
        self.results_txt.grid(row = 1, column = 1, columnspan = 1, rowspan = 10)

        # create list of player results
        # each row represents the results of a presented configuration
        # each row contain:
        # column 0 correct_column   values 1,2 3,4 or 0 if game not yet run
        # column 1 player_answer    values 1,2,3,4 or 0(if no answer given)
        # column 2 player_correct   value       True if player_answer = correct_column
        #                           otherwise   False
        # column 3 player_time      time the player took to press button or
        #                           the maximum time(i.e.speed chosen) + 1 if timed out
        
        self.player_results= [[0,0,0,-1],# element 0 not used
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],#60
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],#120
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],#180
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],#240
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],[0,0,0,-1],#252
                              [0,0,0,-1],[0,0,0,-1],[0,0,0,-1]]

        # create list of leds to be lit for a configuration 
        #
        #the number of LEDs to be lit in each column
        self.LEDs_in_column = [0,0,0,0]

        # rows 1-8 :a list of up to 8 LEDs for each column which need to be lit
        self.random_LEDs =[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],
                          [0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    # ................. end of method: create widgets .................
 
    #.................... Method: start_game ................
    # This method sets the time interval and number of configurations
    # chosen by the player. then lights turns on and off each quadrant
    # of the LEDs until the player presses the gameboard start button.
    # then runs the game.
    #
    def start_game(self):
        status= ""
        self.choices_txt.delete(CSTARTED_ROW, END)
        self.choices_txt.insert(CSTARTED_ROW, status)
        self.timeout = 0
        self.quadrant_circuit =0
        self.quadrant_timer = 0
        self.StartButton_pressed = False  # True if START button on screen is pressed
        self.StopSwitch  = False          # True if STOP switch on game is pressed
        self.Switch_pressed = False       # True if STOP button or Stop Switch or any column button is pressed
        count = 1
        #first empty the results table ready for new results
        for config in range (1,255):
            self.player_results[config][C_correct_column] = 0
            self.player_results[config][C_player_answer] = 0
            self.player_results[config][C_player_correct] = 0
            self.player_results[config][C_player_time] = -1

        # next make sure all LEDs are off
        self.turnall_off()
        # clear the statistics and results tables ready for new stats and results
        self.stats_txt.delete(0.0, END)
        self.results_txt.delete(0.0, END)

        #then start the quadrant pattern
        # whilst not timed out and start switch not pressed
        while (self.timeout < 1050                      # Player hasn't timedout
               and self.StartButton_pressed== False     # player hasn't pressed Start Switch
               and self.StopSwitch == False):           # player hasn't pressed Stop Switch
            # get current state of switches
            self.StartButton_pressed = pfio.digital_read (CSTARTBUTTON, CBOARDwithBUTTONS);
            self.StopSwitch  = pfio.digital_read (CSTOPBUTTON , CBOARDwithBUTTONS);
            if self.StartButton_pressed == False and self.StopSwitch ==False :
                if self.quadrant_timer == 0:
                   self.quadrant_on_off ( 4 , CLEDOFF )
                   self.quadrant_on_off ( 1 , CLEDON )
                   self.quadrant_circuit = 2
                elif self.quadrant_timer == 50:
                    self.quadrant_on_off ( 1 , CLEDOFF )
                    self.quadrant_on_off ( 2 , CLEDON )
                    self.quadrant_circuit = 3

                elif self.quadrant_timer == 100:
                    self.quadrant_on_off ( 2 , CLEDOFF )
                    self.quadrant_on_off ( 3 , CLEDON )
                    self.quadrant_circuit = 4

                elif self.quadrant_timer == 150:
                    self.quadrant_on_off ( 3 , CLEDOFF )
                    self.quadrant_on_off ( 4 , CLEDON )
                    self.quadrant_circuit = 1
                    
                elif self.quadrant_timer == 199 :
                    self.quadrant_timer = -1
                
            self.timeout = self.timeout +1
            self.quadrant_timer = self.quadrant_timer +1
            sleep(0.01)

        if self.timeout == 1050: # player hasn't pressed start quick enough
            status = status + "\nGame Start Timeout"
            status = status + " - press the Game board start button quicker!"
            self.choices_txt.delete(CSTARTED_ROW, END)
            self.choices_txt.insert(CSTARTED_ROW, status)
            self.turnall_off()
        elif self.StopSwitch == True : # player has pressed Stop Switch
            self.stop_game()
            status = "\nGame stopped"
            self.choices_txt.delete(CSTOPPED_ROW, END)
            self.choices_txt.insert(CSTOPPED_ROW, status)
            self.stats_txt.delete(0.0, END)
            self.results_txt.delete(0.0, END)
        else: # player has pressed start switch
            status = "\nGame started"
            self.choices_txt.delete(CSTARTED_ROW, END)
            self.choices_txt.insert(CSTARTED_ROW, status)
            self.stats_txt.delete(0.0, END)
            self.results_txt.delete(0.0, END)
            while self.StopSwitch == False and count <self.configs+1:
                self.generate_random_LEDs(count)
                self.process_config(count, self.speed)
                count = count +1
            self.calculate_results(count-1, self.speed)
            self.calculate_statistics(count-1, self.speed)
            
    # ................. end of method: start_game .................

     
    #.................... Method: choose_game_setup ................
    # This method validates and sets the speed and number of
    # configurations chosen by the player.
    # it reads in the values typed on the screen by the player.
    # If the format of the input is wrong ( eg 3p instead of 30 )
    # or too big or too small a value is given then the default value is used
    # 
    
    def choose_game_setup(self):
        status = ""
        # first get no of configs
        contents = self.configs_ent.get()            
        try:
            self.configs = int(contents)
        except:
            self.configs = CMAXCONFIGS + 1

        if self.configs<1 or self.configs>CMAXCONFIGS:
            # number given out of bounds so set to default 10
            self.configs = CDEFAULTCONFIGS
            status = status + "Invalid Number of Game configurations chosen.\n   Default used - set at "
            status = status + str(self.configs)
        else:
            status = status + "Number of Game configurations chosen :" + str(self.configs)

        #now get speed
        contents = self.speed_ent.get()
        try:
            self.speed = int(contents)
        except:
            self.speed = CDEFAULTSPEED+1

        if self.speed<200 or self.speed>CDEFAULTSPEED:
            # number given out of bounds so set to default speed
            self.speed = CDEFAULTSPEED 
            status = status + "\nInvalid game speed chosen. \n   Default used - set at " + str(self.speed)
        else:
            status =status = status + "\nGame speed chosen : " + str(self.speed)
        status = status +"\nReady to start"

        self.choices_txt.delete(CCONFIGS_ROW, END)
        self.choices_txt.insert(CCONFIGS_ROW, status)
        self.stats_txt.delete(0.0, END)
        self.results_txt.delete(0.0, END)

    # ................. end of method: choose_game_setup .................


    #.................... Method: stop_game ................
    # This method stops the current game in play.
    #
    def stop_game(self):
        status = ""
        self.Stopswitch = True
        self.Switch_pressed = False
        self.turnall_off()
        status = "\nGame stopped"
        
        self.choices_txt.delete(CSTOPPED_ROW, END)
        self.choices_txt.insert(CSTOPPED_ROW, status)

    # ................. end of method: stop_game .................
    
    #.................... Method: turnall_off ................
    # This method turns all the LEDs on all four boards OFF
    #
    def turnall_off(self):
        # for each LED on each BOARD turn the led off
        for led in range (0,8,1):
            for board in range (0,4,1):
                pfio.digital_write(led,CLEDOFF,board)      
    # ................. end of method: turnall_off .................

    #.................... Method: quadrant_on_off ................
    # This method turns on or off all the LEDs in a quadrant of the board.
    # 1 = Top Left Quadrant     = LEDs 4 to 7 on boards 0 and 1
    # 2 = top right quadrant    = LEDs 4 to 7 on boards 2 and 3
    # 3 = bottom right quadrant = LEDs 0 to 3 on boards 2 and 3
    # 4 = bottom left quadrant  = LEDs 0 to 3 on boards 0 and 1
    # It is passed the following parameters:
    #   - quadrant = the quadrant number
    #   - on_off   = whether the quadrant should be turned ON = 1 or OFF = 0
    #
    def quadrant_on_off(self, quadrant, on_off):
        status = ""
        if quadrant == 1:
            startled = 4
            startboard = 0
        elif quadrant == 2 :
            startled = 4
            startboard = 2
        elif quadrant == 3 :
            startled = 0
            startboard = 2
        elif quadrant == 4 :
            startled = 0
            startboard = 0
        else :
            startled = 4
            startboard = 0
        for led in range (startled,startled+4,1):
            for board in range ( startboard, startboard+2, 1):
                pfio.digital_write ( led, on_off, board )
      
    # ................. end of method: quadrant_on_off.................

       
    """.................... Method: process_config ................
    # This method sets the LEDs for this configuration and then waits for a switch
    # to be pressed or a timeout to occur, then updates the player results table
    # It is passed
    #   - configno : the number of the configuration currently being played
    #   - speed : the speed the player chose , and hence the timeout too

    """
    def process_config(self,configno,speed):
        """ Process the next configuration. """

        self.timeout = 0
        self.Switch_pressed = False
        
        # whilst not timed out and no column switch has been pressed
        while self.timeout < speed and self.Switch_pressed== False :
            # update the timeout counter 
            self.timeout = self.timeout +10
            # get current state of the 4 column choice switches
            self.ColumnSwitch1 = pfio.digital_read (CLEDCOL1_BUTTON, CBOARDwithBUTTONS);
            self.ColumnSwitch2 = pfio.digital_read (CLEDCOL2_BUTTON, CBOARDwithBUTTONS);
            self.ColumnSwitch3 = pfio.digital_read (CLEDCOL3_BUTTON, CBOARDwithBUTTONS);
            self.ColumnSwitch4 = pfio.digital_read (CLEDCOL4_BUTTON, CBOARDwithBUTTONS);
            # and get current state of the STOP switche
            self.StopSwitch = pfio.digital_read (CSTOPBUTTON, CBOARDwithBUTTONS);

            # check which column was chosen
            if self.StopSwitch == True :
                self.Switch_pressed = True               
            else:
                if (self.ColumnSwitch1 ==True or self.ColumnSwitch2 ==True or
                    self.ColumnSwitch3 ==True or self.ColumnSwitch4 == True ):
                    # check which button and hence which column chosen
                    if self.ColumnSwitch1:
                        # put the chosen column no in the players stats table
                        self.player_results[configno][C_player_answer] = 1
                    elif self.ColumnSwitch2:          
                       # put the chosen column no in the players stats table
                        self.player_results[configno][C_player_answer] = 2
                    elif self.ColumnSwitch3 :          
                      # put the chosen column no in the players stats table
                        self.player_results[configno][C_player_answer] = 3
                    elif self.ColumnSwitch4:          
                       # put the chosen column no in the players stats table
                        self.player_results[configno][C_player_answer] = 4

                    # set button pressed to show that a column has been chosen
                    self.Switch_pressed = True
                    # put the time taken in the players stats table
                    self.player_results[configno][C_player_time] = self.timeout
                    # check if the chosen column is correct and update the players stats table
                    if self.player_results[configno][C_player_answer] == self.player_results[configno][C_correct_column]:
                        self.player_results[configno][C_player_correct] = True
                    else:
                        self.player_results[configno][C_player_correct] = False
                # update the timeout counter 
                self.timeout = self.timeout +10
                # sleep for 0.01s before testing again
                sleep(0.01)
                
        # if the player has not pressed a button before the timeout then
        # the player stats need to be updated to show Timeout.
        if self.StopSwitch == True or self.Switch_pressed == False :
            # put the column no  0 in the players stats table to indicate Timeout
            self.player_results[configno][C_player_answer] = 0
            # set the player correct indicator to False
            self.player_results[configno][C_player_correct] = False
            # set the players time to speed to indicate timeout
            self.player_results[configno][C_player_time] = speed + 1
        
        if self.StopSwitch == True:
            self.stop_game()
            
        self.turnall_off()        

    # end of method: process_config..............................

    """.................... Method: generate_random_LEDs ................
    # This method generates a random selection of LEDs in each of the four columns.
    # It generates 4 unique random numbers to represent the number
    # of LEDs in each of the 4 Columns
    # For each of those random numbers it generates that many random LED choices for that column.
    # It ensure all LEDs are off, then turns on the selected LEDs in each column.
    It is passed configno = the number of the current configuration being worked on
    """
    def generate_random_LEDs(self,configno):
        """ Generate  random numbers """
        
        # First decide how may LEDs in which Columns to turn ON
        # generate random numbers for each column
        self.LEDs_in_column[0] = random.randint(1,8)
        self.LEDs_in_column[1] = random.randint(1,8)
        self.LEDs_in_column[2] = random.randint(1,8)
        self.LEDs_in_column[3] = random.randint(1,8)
        #now check they are all different
        while self.LEDs_in_column[1] == self.LEDs_in_column[0]:
            self.LEDs_in_column[1] = random.randint (1,8)
        while (self.LEDs_in_column[2] == self.LEDs_in_column[0] or
            self.LEDs_in_column[2] == self.LEDs_in_column[1]):
            self.LEDs_in_column[2] = random.randint(1,8)
        while (self.LEDs_in_column[3] == self.LEDs_in_column[0] or
        self.LEDs_in_column[3] == self.LEDs_in_column[1] or
        self.LEDs_in_column[3] == self.LEDs_in_column[2]):
            self.LEDs_in_column[3] = random.randint(1,8)

        # update the payer results table to show which column is the correct answer
        if (self.LEDs_in_column[0] > self.LEDs_in_column[1] and
            self.LEDs_in_column[0] > self.LEDs_in_column[2] and
            self.LEDs_in_column[0] > self.LEDs_in_column[3]):
            # then 1st column has most LEDs
            self.player_results[configno][C_correct_column] = 1
        elif (self.LEDs_in_column[1] > self.LEDs_in_column[0] and
            self.LEDs_in_column[1] > self.LEDs_in_column[2] and
            self.LEDs_in_column[1] > self.LEDs_in_column[3]):
            # then 2nd column has most LEDs
            self.player_results[configno][C_correct_column] = 2
        elif (self.LEDs_in_column[2] > self.LEDs_in_column[0] and
            self.LEDs_in_column[2] > self.LEDs_in_column[1] and
            self.LEDs_in_column[2] > self.LEDs_in_column[3]):
            # then 3rd column has most LEDs
            self.player_results[configno][C_correct_column] = 3    
        elif (self.LEDs_in_column[3] > self.LEDs_in_column[0] and
            self.LEDs_in_column[3] > self.LEDs_in_column[1] and
            self.LEDs_in_column[3] > self.LEDs_in_column[2]):
            # then 4th column has most LEDs
            self.player_results[configno][C_correct_column] = 4

        # now generate which LED numbers for each column
        # first set all LED numbers to unique negative numbers
        # so all off and all different
        for row in range (0,8):
            for column in range (0,4):
                self.random_LEDs [row][column] =-1 * row

        # now generate all the random LED nos
        for column in range (0,4) :
            # for each column generate  random LED numbers
            for row in range (0,self.LEDs_in_column[column]):
                self.random_LEDs[row][column]= random.randint(1,8)
                
            #now check the LED numbers in this column are all different
            if self.LEDs_in_column[column] >1:
                #While 2nd choice is same as first
                while self.random_LEDs [1][column] == self.random_LEDs [0][column]:
                    # change 2nd choice
                    self.random_LEDs [1][column] = random.randint (1,8)
 
            if self.LEDs_in_column[column] >2:
                #whilst 3rd choice is same as 1st or 2nd
                while (self.random_LEDs [2][column] == self.random_LEDs [0][column] or
                    self.random_LEDs [2][column] == self.random_LEDs [1][column]):
                    # change 3rd choice
                    self.random_LEDs [2][column] = random.randint(1,8)

            if self.LEDs_in_column[column] >3:
                #whilst 4th choice is same as 1st or 2nd or 3rd
                while (self.random_LEDs [3][column] == self.random_LEDs [0][column] or
                self.random_LEDs [3][column] == self.random_LEDs [1][column] or
                self.random_LEDs [3][column] == self.random_LEDs [2][column]):
                    # change 4th choice
                    self.random_LEDs [3][column] = random.randint(1,8)
    
            if self.LEDs_in_column[column] >4:
                #whilst 5th choice is same as 1st 2nd 3rd or 4th
                while (self.random_LEDs [4][column] == self.random_LEDs [0][column] or
                self.random_LEDs [4][column] == self.random_LEDs [1][column] or
                self.random_LEDs [4][column] == self.random_LEDs [2][column] or
                self.random_LEDs [4][column] == self.random_LEDs [3][column]):
                    #change 5th choice
                    self.random_LEDs [4][column] = random.randint(1,8)

            if self.LEDs_in_column[column] >5:
                # whilst 6th choice is same as 1st 2nd 3rd 4th or 6th
                while (self.random_LEDs [5][column] == self.random_LEDs [0][column] or
                self.random_LEDs [5][column] == self.random_LEDs [1][column] or
                self.random_LEDs [5][column] == self.random_LEDs [2][column] or
                self.random_LEDs [5][column] == self.random_LEDs [3][column] or
                self.random_LEDs [5][column] == self.random_LEDs [4][column]):
                    # change 6th choice
                    self.random_LEDs [5][column] = random.randint(1,8)

            if self.LEDs_in_column[column] >6:
                # whilst 7th choice is same as 1st 2nd 3rd 4th 5th or 6th
                while (self.random_LEDs [6][column] == self.random_LEDs [0][column] or
                self.random_LEDs [6][column] == self.random_LEDs [1][column] or
                self.random_LEDs [6][column] == self.random_LEDs [2][column] or
                self.random_LEDs [6][column] == self.random_LEDs [3][column] or
                self.random_LEDs [6][column] == self.random_LEDs [4][column] or
                self.random_LEDs [6][column] == self.random_LEDs [5][column]):
                    # change 7th choice
                    self.random_LEDs [6][column] = random.randint(1,8)
 
            if self.LEDs_in_column[column] ==8:
                # whilst 8th choice is same as 1st 2nd 3rd 4th 5th 6th or 7th
                while (self.random_LEDs [7][column] == self.random_LEDs [0][column] or
                self.random_LEDs [7][column] == self.random_LEDs [1][column] or
                self.random_LEDs [7][column] == self.random_LEDs [2][column] or
                self.random_LEDs [7][column] == self.random_LEDs [3][column] or
                self.random_LEDs [7][column] == self.random_LEDs [4][column] or
                self.random_LEDs [7][column] == self.random_LEDs [5][column] or
                self.random_LEDs [7][column] == self.random_LEDs [6][column]):
                    # change 8th choice
                    self.random_LEDs [7][column] = random.randint(1,8)
        
        # First make sure all LEDS are OFF 
        self.turnall_off()
        # wait one second
        sleep(1)
        # then turn on the chosen LEDs
        for board in range (0,4):
            for choice in range ( 0, self.LEDs_in_column[board]):
                pfio.digital_write ( self.random_LEDs[choice][board]-1, CLEDON, board )
                   
    # ..................... end of method : generate_random_LEDs .........




    #.................... Method: calculate_statistics ................
    # This method works out the player statistics at the end of a game
    # and puts the statistics in the stats panel.
    # It displays for each configuration played:
    #   - the number and percentage of configurations the player got right
    #   - the number and percentage of configurations the player got wrong
    #   - the number and percentage of configurations the player timed out
    #   - the number and percentage of configurations in total
    #   - the average time the player took to choose a column or Timeout
    # It is passed
    #   - configs : the number of configurations that were played
    #   - speed : the speed the player chose , and hence the timeout too
    #
    def calculate_statistics(self, configs, speed):
        """ Update text widget and display LED states. """
        averagetime = 0.0
        totaltime = 0
        timeout_count = 0
        correct_count = 0
        wrong_count = 0
        timeout_stat = 0.0
        correct_stat = 0.0
        wrong_stat = 0.0
        stats=""
        stats = "Statistics : \n"
        if self.StopSwitch == False:
            choices = "\nGame finished"
            self.choices_txt.delete(CSTOPPED_ROW, END)
            self.choices_txt.insert(CSTOPPED_ROW, choices)
        
        # work out number of Timeouts and average time
        for config in range (1,configs+1):
            # work out number of timeouts
            if self.player_results[config][C_player_time]>speed:
                timeout_count= timeout_count + 1
            # add up all the time scores
            totaltime = totaltime + self.player_results[config][C_player_time]
            # add up how many correct
            if self.player_results[config][C_player_correct]==True:
                correct_count= correct_count + 1
                     
        averagetime = 0.001*totaltime/configs;
        wrong_count = configs - correct_count - timeout_count
        wrong_stat   = wrong_count   * 100 / configs
        correct_stat = correct_count * 100 / configs
        timeout_stat = timeout_count * 100 / configs
        
        stats = stats + "\nCorrect\t\t"+ str(correct_count)+"\t\t" + str(int(correct_stat)) + "%"
        stats = stats + "\nWrong\t\t" + str(wrong_count)+"\t\t" + str(int(wrong_stat)) + "%"
        stats = stats + "\nTimeout\t\t" + str(timeout_count)+"\t\t" + str(int(timeout_stat)) + "%"
        stats = stats + "\nTotal\t\t" + str(configs)+"\t\t" + "100%"
        stats = stats + "\n\nAverage time\t\t" + str(averagetime) +" seconds\n"
         
        self.stats_txt.delete(0.0, END)
        self.stats_txt.insert(0.0, stats)

    # end of method: update_stats..............................
    
    #.................... Method: calculate_results ................
    # This method puts the players results i the results panel.
    # It displays for each configuration played:
    #   - the number of the configuration
    #   - the column the player should have chosen
    #   - the column the player did chose
    #   - whether the player was correct
    #   - the time the player took to choose a column or Timeout
    #
    def calculate_results(self, configs, speed):
        """ Display the results. """
        ptime = 0.0
        status=""
        status = "Results : \n"

        status = status + "Config\tCorrect\tPlayer\tCorrect\tPlayer\n"
        status = status + "Number\tColumn\tChoice\tY/N\tTime\n"
        for config in range (1,configs+1):
            status = status + "\n" + str(config) + "\t"
            status = status + str(self.player_results[config][C_correct_column])+ "\t"
            status = status + str(self.player_results[config][C_player_answer] )+ "\t"
            if self.player_results[config][C_player_correct]==True:
                status = status +  "Y\t"
            else:
                status = status +  "N\t"
            if self.player_results[config][C_player_time]> speed:
                status = status +"Timeout"
            else:
                ptime = self.player_results[config][C_player_time]*0.001
                status = status + str(ptime)           
            
        self.results_txt.delete(0.0, END)
        self.results_txt.insert(0.0, status)

        # end of method: calculate_results..............................

#=================================================================
# main
#=================================================================

root = Tk()                             # Create the GUI root object
root.title("LED Counting Game")
app = Application(root)                 # Create the root application window
root.mainloop()
