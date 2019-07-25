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

def just_a_bunch_o_buttons_n_stuff(bees):
    
    if bees == 1:
        app.addLabel("test label", "Well look who it is.")   
        app.addLabel("testes label", "bees")    
        app.addButtons(["btn1","btn2"], do_nothing )
    
    if bees == 2:
        app.addEntry("Bees?")
        app.addLabel("Beeeees","Bees")
   
    if bees == 3:
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
        app.setMeter('initialization progress',100)
        display_window("Main Screen", False)
        app.destroySubWindow("Main Screen")
        load_data_win()
        app.show()
    else:
        print("Please choose a file before loading ")
    
    
def exit_main():
    app.destroySubWindow("Main Screen")
    app.stop()    
    
    
# MAIN WINDOW
def load_main_win():
    
    app.startSubWindow("Main Screen", "1200x800")
    # LOGO
    app.startFrame('main_header',0,0)
    app.addImage("Logo",logo_in, compound=None)
    app.stopFrame()
    
    # LOAD FILE
    app.addFileEntry("load file",)
    app.setEntryDefault("load file", "- Choose a file -")
    app.addButton("Generate", initialize_dataset)
    
    # INIT/EXIT BTNS
    app.addMeter("initialization progress")
    app.setMeterFill("initialization progress", "light blue")
    app.addButton("Exit", exit_main, app.getRow(),3)
    
    app.stopSubWindow()
    

    
    
# DATA OVERVIEW/NAVIGATION WINDOW    
def load_data_win():
    app.startTabbedFrame("Data Win Tabs")
    
    app.startTab("Overview")
    just_a_bunch_o_buttons_n_stuff(1)
    app.stopTab()
    
    app.startTab("States")
    just_a_bunch_o_buttons_n_stuff(2)
    app.stopTab()
    
    app.startTab("Category")
    just_a_bunch_o_buttons_n_stuff(3)
    app.stopTab()

    app.stopTabbedFrame()
    app.setTabbedFrameTabExpand("Data Win Tabs", expand=True)





def display_window(window_name, hidden=False):
    if not hidden:
        app.showSubWindow(window_name)
    else:
        app.hideSubWindow(window_name)        
    


    
    
# Create gui object to hold windows
app = gui("Subsidy Calculator","900x600")

load_main_win()

app.go(startWindow="Main Screen")

