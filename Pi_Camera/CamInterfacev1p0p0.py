#!/usr/bin/env python

#==============================================================
#
# Authors:      Christine Smythe and Colin Smythe (Dunelm Services Limited)
# Version:      1.0
# Release Date: 6th January, 2014
#
# Description:  This simple Python3 program is used to take a single photo,
#               multiple photos or a video with the RPi-Camera
#               This program requires Python3.
#
#               For a single photo the user needs to enter a filename eg myphoto
#               to which the program will add .jpg
#               The file wil be created in the users current directory -
#               so make sure you are in the right current working
#               directory before running the program.
#               If you chose a filename already in use the contents will be
#               overwritten by the new photo
#
#               For multiple photos the user needs to specify
#               -   a directory name to store the new images in eg myphotos: this
#                   must be a new directory not one already in use because the
#                   program will create the new directory for the photos.
#               -   the number of images to take : default is 1
#                   The images will be named image00001.jpg, image00002.jpg, etc
#               -   the number of seconds to wait between images : default is 1 second
#
#               For a video the user needs to specify a filename eg myvideo to which
#               the program will add .h264
#               then press 'Start video' to start recording and
#               'Stop video' to stop recording.
#
#               Please ensure you press 'QUIT' rather than closing the window in order to 
#               cleanly close the camera preview window.
#
#               If you want to view any of the images then simply use the file manager and
#               double click on the filename. This doesn't work for videos.
#
# History:      Original release.
#
# Copyright:    2013 (c) Premier Farnell Limited
#
# License:      GPLv3+
#
#==============================================================

from tkinter import *
from tkinter import messagebox
from time import sleep
import picamera
import os

#==============================================================
# Declaration of Constants
# none used

#==============================================================

class Application(Frame):
    """ GUI Application for taking photos. """

    def __init__(self, master):
        super(Application, self).__init__(master)  
        self.grid()
        self.create_widgets()
        self.setup_camera()

    #.................Method: create widgets..........................
    # This creates a window with buttons 
    #   - to take a single photo, multiple photos or a video.
    #   SA single photo just needs the user to enter a filename to put
    #   the photo in. The filename is appended with .jpg and the file
    #   placed in the users current directory.
    #   Multiple photos need the ueer to specify a new directory name to
    #   store the photos in. The new directory will be created in the users
    #   current directory and images named imagexxxxx.jpg will be created
    #   within the new direcory.
    #   A video needs a filename to store the video in adn again will be
    #   created in the users current directory.
    #
    def create_widgets(self):
        """ Create widgets for photos. """    

        # create variable for radio buttons to share to note which mode has been selected
        self.mode = StringVar()
        self.mode.set(None)

        #setup widget to get filename for single photo
        Label(self, text = "Take Photos").grid(row = 0, column = 0, sticky = W+E+N+S, columnspan=2)

        # create 'TAKE A SINGLE PHOTO' button
        Radiobutton( self,
                text = "Take a Single Photo",
                variable = self.mode,
                value = "single",
                command = self.choose_single_photo,
                bg='blue',
                ).grid(row=1, column = 0, sticky = W+E+N+S)

        # create 'TAKE MULTIPLE PHOTOS' button
        Radiobutton( self,
                text = "Take multiple Photos",
                variable = self.mode,
                value = "multiple",
                command = self.choose_multiple_photos,
                bg='blue',
                ).grid(row=1, column = 1, sticky = W+E+N+S)

        #setup widgets to get directory name for multiple photos
        Label(self, text = "Directory name:").grid(row = 2, column = 1, sticky = W+E+N+S)
        self.m_filename = Entry(self)
        self.m_filename.grid(row = 3, column = 1)
        
        #setup widgets to get filename for single photo
        Label(self, text = "Photo Filename:").grid(row = 2, column = 0, sticky = W+E+N+S)
        self.s_filename = Entry(self)
        self.s_filename.grid(row = 3, column = 0)

        #setup widgets to get number of images for multiple photos
        Label(self, text = "Number of images:").grid(row = 4, column = 1, sticky = W+E+N+S)
        self.m_num = Entry(self, width = 5)
        self.m_num.grid(row = 5, column = 1 )
          
        #setup widgets to get frequency of images for multiple photos
        Label(self, text = "Seconds between images:").grid(row = 6, column = 1, sticky = W+E+N+S)
        self.m_secs = Entry(self, width = 6)
        self.m_secs.grid(row = 7, column = 1)

        # create 'ACTION' button
        Button( self,
                text = "Camera, Lights, ACTION!",
                command = self.action_camera,
                bg='blue',
                ).grid(row=8, column = 0, sticky = W+E+N+S, columnspan=2)

        #setup widgets for video
        Label(self, text = "Shoot a Video").grid(row = 0, column = 2, sticky = W+E+N+S)

        #setup widgets to get filename for video
        Label(self, text = "Video Filename :").grid(row = 2, column = 2, sticky = W+E+N+S)
        self.v_filename = Entry(self)
        self.v_filename.grid(row = 3, column = 2)

        # create 'Start Video' button
        Button( self,
                text = "Start video",
                command = self.start_video,
                bg='green',
                ).grid(row=6, column = 2, sticky = W+E+N+S)

        # create 'Stop video' button
        Button( self,
                text = "Stop Video",
                command = self.stop_video,
                bg='green',
                ).grid(row=7, column = 2, sticky = W+E+N+S)
        
        # create 'QUIT' button
        Button( self,
                text = "QUIT",
                command = self.exit_camera,
                bg='red',
                ).grid(row=8, column = 2, sticky = W+E+N+S)
       
        # create text field to display results
        self.results_txt = Text(self, height = 8, wrap = WORD)
        self.results_txt.grid(row = 9, column = 0, columnspan =3)

    #.................... Method: choose_single_photo ................
    # This method selects the single photo option
    # and asks the user to enter a filename and press ACTION 
    #
    def choose_single_photo(self):
        self.chosenfile = StringVar()
        self.chosenfile.set(None)
        status = ""
        status = "You have chosen to take a single photo.\n"
        status = "Make sure you have entered a filename then\n"
        status += "press 'Action' when ready\n" 
        self.results_txt.delete(0.0, END)
        self.results_txt.insert(0.0, status)        
 
    # ................. end of method choose_single_photo .................

    #.................... Method: choose_multiple_photos ................
    # This method selects the multiple photos option
    # and asks the user to enter a directory name,
    # time in seconds between photos and
    # how many photos to take
    #
    def choose_multiple_photos(self):
        status = ""
        status = "You have chosen to take multiple photos.\n"
        status += "Don't forget to choose a filename, how many images and how many seconds between images "
        status += "then press 'Action' when ready\n"
        self.results_txt.delete(0.0, END)
        self.results_txt.insert(0.0, status)
 
    # ................. end of method choose_multiple_photos .................


    #.................... Method: action_camera ................
    # This method calls appropriate method depending on which
    # photo option user has chosen
    #
    def action_camera(self):
        status = ""
        if self.mode.get() == "single" :
             self.action_single()
        elif self.mode.get() == "multiple":
            self.action_multiple()
        else:
            status += "Whoops! Wrong mode. Something went wrong!\n"
            self.results_txt.delete(0.0, END)
            self.results_txt.insert(0.0, status)
    

    # ................. end of method action camera .................

    #.................... Method: action_multiple ................
    # This method takes multiple photos
    # and updates the status display to show the name of the file it is saved in
    #
    def action_multiple(self):
        status = ""
        numphotos = 1
        numsecs = 1
        chosenfile = ""
        ferror = 0
        
        #first get filename
        contents= self.m_filename.get()
        self.chosenfile= str(contents)
        status = "chosen directory name : " + self.chosenfile + "\n"

        try:
            # first create the directory to store the photos in
            os.mkdir(self.chosenfile)
        except:
           # can't create the directory
           status += "Invalid file namechosen - " + chosenfile + "\n"
           ferror = 1
        
        if ferror == 0 :
           # have created directory ok so
           # next get no of photos
            contents = self.m_num.get()            
            try:
                self.numphotos = int(contents)
            except:
                self.numphotos = 1
                status = status + "Invalid Number of photos chosen - Set at 1.\n"

            if self.numphotos<1 :
                # number given out of bounds so set to default 1
                self.numphotos = 1
                status = status + "Invalid Number of photos chosen - Set at 1.\n"
            else:
                status = status + "Number of photos chosen : " + str(self.numphotos) + "\n"

            # now get no of seconds between photos
            contents = self.m_secs.get()            
            try:
                self.numsecs = int(contents)
            except:
                # invalid number format
                self.numsecs = 1
                status = status + "Invalid time interval chosen - Set at 1.\n"

            if self.numsecs<1 :
                # number given out of bounds so set to default 1
                self.numsecs = 1
                status = status + "Invalid time interval chosen - Set at 1.\n"
            else:
                status = status + "Time interval chosen : " + str(self.numsecs) + "\n"

            # now take the photos
            try:
                for i, filename in enumerate(self.camera.capture_continuous(self.chosenfile+'/image{counter:05d}.jpg')):
                    sleep(self.numsecs)
                    status += 'captured image %s' % filename + "\n"
                    if i==(self.numphotos-1):
                        break
            except:
               status += "Invalid file namechosen - " + chosenfile + "\n"

        self.results_txt.delete(5.0, END)
        self.results_txt.insert(5.0, status)

    # ................. end of action_multiple .................
    
    #.................... Method: action_single ................
    # This method takes a single photo
    # and updates the status display to show the name of the file it is saved in
    #
    def action_single(self):
        status = ""
        numphotos = 1
        numsecs = 1
        chosenfile = ""

        #first get filename
        contents= self.s_filename.get()
        #convert to string and add .jpg
        self.chosenfile= str(contents)+ ".jpg"
        status = "\nchosen filename : " + self.chosenfile + "     "

        #now take photo
        try:
            self.camera.capture(self.chosenfile)
            status += "captured image - " + self.chosenfile
        except:
           status += "Invalid file namechosen - " + self.chosenfile

        self.results_txt.delete(5.0, END)
        self.results_txt.insert(5.0, status)

    # ................. end of action_single .................
    
    
    #.................... Method: start_video ................
    # This method gets the filename the user has entered, starts the video
    # and updates the status display to show the name of the file it is saved in
    #
    def start_video(self):
        status = ""
        chosenfile = ""

        #first get filename
        contents= self.v_filename.get()
        #convert to string and add .h264 for file format
        self.chosenfile= str(contents) + ".h264"
        status = "chosen filename : " + self.chosenfile + "\n"
 
        # now start the recording
        try:
            status += "\nStarting to record   \n"
            self.camera.start_recording(self.chosenfile)
        except:
            status += "Invalid file name chosen - " + self.chosenfile + "\n"          

        self.results_txt.delete(0.0, END)
        self.results_txt.insert(0.0, status)

    # ................. end of start_video .................
    

    #.................... Method: stop_video ................
    # This method stops the video recording
    # and updates the status display 
    #
    def stop_video(self):
        status = ""
        chosenfile = ""
        try:
            self.camera.stop_recording()
            status += "stopped recording \n " 
        except:
            status += "Error on stop recording \n"     

        self.results_txt.delete(6.0, END)
        self.results_txt.insert(6.0, status)

    # ................. end of stop_video .................
    
      
    #.................... Method: exit_camera ................
    # This method closes down the camera nicely and exits
    #
    def exit_camera(self):
        status = ""
        useranswer = ""
        useranswer = "no"
        cancelquestion = "You are still recording a video.\nDo you wish to stop recording ?"

        #first check to see if camera is currently recording a video
        if self.camera.recording == True:
            # yes it is recording so ask user if they wish to stop recording
            useranswer=messagebox.askquestion("Exit Error!",
                                         cancelquestion)
            if useranswer == "yes" :
                #if user says yes- stop then stop the recording and cleanup for exit
                self.camera.stop_recording()
                self.camera.stop_preview()
                self.camera.close()
                root.destroy()
            else:
                # otherwise user does not wish to stop so ignore stop request
                status += "continuing recording   \n"
                self.results_txt.delete(7.0, END)
                self.results_txt.insert(7.0, status)
        else :
            # camera isn't currently recording a video so cleanup for exit.
            self.camera.stop_preview()
            self.camera.close()
            root.destroy()


    # ................. end of method: exit_camera .................


    #.................... Method: start_camera ................
    # This method starts the camera.
    #
    def setup_camera(self):
        # instantiate the camera
        self.camera = picamera.PiCamera()
        # change the resolution so it is a smaller window
        # which will fit on screen with GUI window
        self.camera.resolution = (640,480)
        # make it a smaller preview window which will fit on screen with GUI window
        self.camera.preview_fullscreen = False
        self.camera.preview_window = (0,400,400,300)
        self.camera.start_preview()
        #self.results2_txt.delete(0.0, END)
        #self.results2_txt.insert(0.0, status)
        
    # ................. end of method: start_camera .................

             
#=================================================================
# main
#=================================================================

root = Tk()                             # Create the GUI root object
root.title("Image Capture V1.0")
app = Application(root)                 # Create the root application window
root.mainloop()
