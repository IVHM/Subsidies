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
from pandas import Series,DataFrame
from numpy.random import randn

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
    inc = 30
    increment_prog_bar(inc)
    global tot_amt, tot_num, avg_amt

    # The value to increament the progress bar by
    inc = 1
    for state_name in state_instance_dict['State']:
        print("current state: ", state_name, "\n dataloader view of prog bar:",
              app.getMeter("initialization progress"),
              "\nincreament value:", inc)

        crnt_state = States(state_name)
        crnt_state.populate_data(master_df)
        state_instances.append(crnt_state)

        # Calculate the total subsidy values
        tot_amt += crnt_state.total_subsidies

        # Here we increment the progress bar
        increment_prog_bar(inc)

    tot_num = master_df.shape[0]

    avg_amt = tot_amt / tot_num


# Does Nothing / Used for calling template buttons
def do_nothing():
    pass


def load_plt(coord_r, coord_c, df):
    raise NotImplementedError


def increment_prog_bar(increment):
    new_prog = int(app.getMeter("initialization progress")[1][:2]) + increment
    app.setMeter("initialization progress", new_prog)


# LOAD AND INIT DATA/WINDOWS
def initialize_dataset():

    file_path = app.getEntry("load file")

    if file_path != "- Choose a file -":  # default
        print("intializing contents of file: ", app.getEntry("load file"))

        display_window("Main Screen", False)
        data_loader(file_path)

        increment_prog_bar(5)
         
        load_data_win()
        # Once we've finished loading data finalize prog bar
        app.setMeter('initialization progress', 100)
        app.show()
        app.hideSubWindow("Main Screen")
    else:
        print("Please choose a file before loading ")


def exit_main():
    app.destroySubWindow("Main Screen")
    app.stop()


# MAIN WINDOW
def load_main_win(width, length):
    app.startSubWindow("Main Screen", str(width) + "x" + str(length))

    # LOGO
    app.startFrame('main_header', 0, 0)
    app.addImage("Logo", logo_in, compound=None)
    app.stopFrame()

    # LOAD FILE
    app.addFileEntry("load file",)
    app.setEntryDefault("load file", "- Choose a file -")
    app.addButton("Generate", initialize_dataset)

    # INIT/EXIT BTNS
    app.addMeter("initialization progress", app.getRow(), 0, 1, 3)
    app.setMeterFill("initialization progress", "light blue")
    app.setMeterWidth("initialization progress", width * .75)
    app.addButton("Exit", exit_main, app.getRow(), 3)

    app.stopSubWindow()


# DATA OVERVIEW/NAVIGATION WINDOW
# Contains the different tabbed views of the data
def load_data_win():
    app.startTabbedFrame("Data Win Tabs")
    
    app.startTab("Overview")

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
    

def load_data():
    raise NotImplementedError


#Temporary values for testing display
overview_T_R_values = DataFrame({"Description": list("abcdefghi"),
                                 "Value": randn(9)})

# TABS FOR DATA WINDOW
def load_overview_tab():
     # Plot viewer
    app.startFrame("Plot", row=0, column=0)
    app.setFrameWidth("Plot",8)
    app.setBg("light blue")
    app.addLabel("-- THIS IS WHERE THE PLOT IMAGE GOES --")
    app.stopFrame()

    # Description data ie. Avg subsidy, top state, largest subsidy
    app.startFrame("Miscelaneaous data labels", row=0, column=8)
    app.setFrameWidth("Miscelaneaous data labels", 1)
    app.setBg("yellow")
    app.label("DESCRIPTION")

    # Adds the description of deach cooresponding value
    cnt = 0
    for label_text in overview_T_R_values["Description"]:
        label_name = "Description_" + str(cnt)
        app.addLabel(label_name, str(label_text))
        cnt += 1

    app.stopFrame()


    # Value data
    app.startFrame("Miscelaneaous data values", row=0, column=9)
    app.setFrameWidth("Miscelaneaous data values", 1)
    app.setBg("yellow")
    app.addLabel("VALUE")

    # Adds the values for each entry
    cnt = 0
    for label_value in overview_T_R_values["Value"]:
        label = "Value_" + str(cnt)
        app.addLabel(label, str(label_value))
        cnt += 1

    app.stopFrame()

    app.addLabel("The bottom row", 0, 5)
    

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


# MAIN DISPLAY VARIABLES
width = 1200
length = 800
main_win_ratio = 0.85
app = gui("Subsidy Calculator", str(width) + "x" + str(height))
load_main_win( width * main_win_ratio, length * main_win_ratio )

app.go(startWindow="Main Screen")
