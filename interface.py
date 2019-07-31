#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:53:02 2019

appJar interface

@author: hmatthyseniv
"""
import state
from state import States
from appJar import gui


# ------- GLOBAL VARIABLES --------

# IMAGE LOCATIONS
logo_in = 'images/temp_logo.gif'

# STATE ABBREVIATIONS
state_instance_dict = state.pd.read_csv("state_abbreviations.csv")

# The columns in the csv that are numerical in type
numerical_columns = [6, 8, 9, 10, 11, 12, 16, 23, 24]

# Contains the csv turned dataframe
master_df = None
state_instances = []  # Stores the
missing_data = None

tot_amt = 0
tot_num = 0
avg_amt = 0


# LOADS THE CLASSES/DATAFRAME
def data_loader(file_in):
    global master_df, missing_data, state_instances
    master_df, missing_data = state.init_master_file(file_in,
                                                     numerical_columns)


    global tot_amt, tot_num, avg_amt
    print("data_loader master df-", master_df)
    for state_name in state_instance_dict['State']:
        crnt_state = States(state_name)
        crnt_state.populate_data(master_df)

        print(crnt_state.total_subsidies)
        tot_amt += crnt_state.total_subsidies
        state_instances.append(crnt_state)

    tot_num = master_df.shape[0]
    print("################",tot_num, master_df.shape,"\n\n")
    avg_amt = tot_amt / tot_num
    print(avg_amt, tot_amt, tot_num)


# Does Nothing / Used for calling template buttons
def do_nothing():
    pass


def load_plt(coord_r, coord_c, df):
    raise NotImplementedError


def increment_prog_bar(increment):
    raise NotImplementedError


# LOAD AND INIT DATA/WINDOWS
def initialize_dataset():

    file_path = app.getEntry("load file")

    if file_path != "- Choose a file -":  # default
        print("intializing contents of file: ", app.getEntry("load file"))
        # TEMPORARY fix for displaying the progress bar
        app.setMeter('initialization progress', 100)
        display_window("Main Screen", False)
        data_loader(file_path)

        load_data_win()
        app.hideSubWindow("Main Screen")
        app.show()
    else:
        print("Please choose a file before loading ")


def exit_main():
    app.destroySubWindow("Main Screen")
    app.stop()


# MAIN WINDOW
def load_main_win():
    app.startSubWindow("Main Screen", "900x600")

    # LOGO
    app.startFrame('main_header', 0, 0)
    app.addImage("Logo", logo_in, compound=None)
    app.stopFrame()

    # LOAD FILE
    app.addFileEntry("load file",)
    app.setEntryDefault("load file", "- Choose a file -")
    app.addButton("Generate", initialize_dataset)

    # INIT/EXIT BTNS
    app.addMeter("initialization progress")
    app.setMeterFill("initialization progress", "light blue")
    app.addButton("Exit", exit_main, app.getRow(), 3)

    app.stopSubWindow()


# DATA OVERVIEW/NAVIGATION WINDOW
# Contains the different tabbed views of the data
def load_data_win():
    app.startTabbedFrame("Data Win Tabs")
    
    app.startTab("Overview")
    app.setTabbedFrameFont("Overview", size=90)
    load_overview_tab()
    app.stopTab()

    app.startTab("States")
    load_states_tab()
    app.stopTab()

    app.startTab("Category")
    load_category_tab()
    app.stopTab()

    app.stopTabbedFrame()
    app.setTabbedFrameTabExpand("Data Win Tabs", expand=True)
    

# TABS FOR DATA WINDOW
def load_overview_tab():
    app.addLabel("Tot dollar amt: $"+str(tot_amt))


def load_states_tab():
    pass


def load_category_tab():
    pass


# Shows or hides the inputed window
def display_window(window_name, hidden=False):
    if not hidden:
        app.showSubWindow(window_name)
    else:
        app.hideSubWindow(window_name)


# Create gui object to hold windows
app = None
master_df = None


# MAIN DISPLAY LOOP
width = 1200
height = 800
app = gui("Subsidy Calculator", str(width) + "x" + str(height))
load_main_win()

app.go(startWindow="Main Screen")
