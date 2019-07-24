#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:53:02 2019

appJar interface

@author: hmatthyseniv
"""

from appJar import gui
from tkinter.filedialog import askdirectory,askopenfilename

#IMAGE LOCATIONS
logo_in = 'images/temp_logo.gif'

#Opens a tkinter dialog to get workign file
def add_file(button):
    #filename = askdirectory()
    filename = askopenfilename()
    print(filename)
    app.setEntry('path', filename)
    app.setLabel("file_check", str(app.getEntry("load a file")))

# 
def generate():
    print("""
          Pretend we're loading up all the data from the csv 
          And turning them into their classes and containers
          weeeeeeee!
          """) 
    crnt_progress = app.getMeter("generation_progress")
    app.setMeter("generation_progress",crnt_progress+10)       
    

def load_main():
    app.startFrame('main_header',0,0)
    app.addImage("Logo",logo_in, compound=None)
    app.stopFrame()


    
    
# Create gui object to hold windows
app = gui("Subsidy Calculator","900x600")

#----Tests
test_label_row = app.getRow()
app.addLabel("file_check", 'Default', test_label_row,0)
app.addLabel('test',"bees", test_label_row,1)

#######Need to fix load image bug
#load_main()
#app.addImage("Logo",logo_in, compound=None)

# Loading file
app.addFileEntry('load a file')
#----Test
app.setLabel("file_check", str(app.getEntry("load a file")))

# GENERATE
app.addButton('generate',generate)



# Progress Bar
app.addMeter("generation_progress")
app.setMeterFill("generation_progress","blue")
app.setMeter("generation_progress",10)
app.go()

