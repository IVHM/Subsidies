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


def do_nothing():
    pass

def just_a_bunch_o_buttons_n_stuff():
    app.addLabel("test label", "Well look who it is.")   
    app.addLabel("testes label", "bees")    
    app.addButtons(["btn1","btn2"], do_nothing )
    app.addEntry("Bees?")
    app.addLabels("Bees","Bees")
    app.startFrame('video killed the radio button')
    app.addRadioButton("bees", "Yes")
    app.addRadioButton("bees", "Most definitely")
    app.addRadioButton("bees", "WHAt??")
    app.addRadioButton("bees", "BEEEEEES!!!!")
    app.stopFrame()



# LOAD AND INIT DATA/WINDOWS 
def initialize_dataset():
    print("""
          Pretend we're loading up all the data from the csv 
          And turning them into their classes and containers
          weeeeeeee!
          """)
    
    
    file_path = app.getEntry("load file")
    if file_path !=  "- Choose a file -": # default
        print("intializing contents of file: ",app.getEntry("load file"))      
        app.setMeter('generation progress',100)
        load_data_win()
    else:
        print("Please choose a file before loading ")
    
    
    
    
    
# MAIN WINDOW
def load_main_win():
    
    app.startSubWindow("Main Screen", "1200x800")
    # LOGO
    app.startFrame('main_header',0,0)
    app.addImage("Logo",logo_in, compound=None)
    app.stopFrame()
    
    # LOAD FILE
    app.addOpenEntry("load file",)
    app.setEntryDefault("load file", "- Choose a file -")
    app.addButton("Generate", initialize_dataset)
    
    # INIT/EXIT BTNS
    app.addMeter("initialization progress")
    app.setMeterFill("initialization progress", "light blue")
    app.addButton("Exit", app.stop, app.getRow(),3)
    
    app.stopSubWindow()
    


    
    
# DATA OVERVIEW/NAVIGATION WINDOW    
def load_data_win():
    app.startSubWindow("data overview","900x600")
    just_a_bunch_o_buttons_n_stuff()
    app.stopSubWindow()
    
    
    
# Create gui object to hold windows
app = gui("Subsidy Calculator","900x600")

load_main_win()


app.go()

