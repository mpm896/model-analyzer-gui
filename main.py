'''
Main script for the IMOD model analyzer GUI

@author: Matt Martinez
'''

import PySimpleGUI as sg
import sys
import setup.initialWindow as initWin
import setup.windowSetup as setWin
import scripts.utils as u
import scripts.setup as setup
import scripts.analyze as a
import itertools
import time

layout = initWin.get_initial_layout()

# Create the window and bind keys
initWindow = sg.Window(title="IMOD Model Analyzer", layout=layout, finalize=True)
initWindow["-MODEL NAME-"].bind("<Return>", "_Enter") # The keybind must be done after the window initialization is finalized

# Initialize the important lists
file_list = []
df_list = []
keys_list = []

# Event loop
while True:
    window, event, values = sg.read_all_windows()

    ###############################################
    ##### ---------- WINDOW EVENTS ---------- #####
    ###############################################

    if event == "Exit" or event == sg.WIN_CLOSED:
        if window == initWindow:
            sys.exit()
        window.close()
    
    # Get model name from the box
    if event == "-MODEL NAME-": 
        model_name = values["-MODEL NAME-"]
    elif event == "-MODEL NAME-" + "_Enter":
        # Get the model files from the given folder
        try:
            file_list = u.read_models(folder, model_name)
        except:
            file_list = []
        initWindow["-FILE LIST-"].update(file_list)

    # Event for folder selection
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]

        # Ensure there is a value for the model name, even if empty
        try:
            model_name
        except NameError:
            model_name = ''

        # Get the model files from the given folder
        try:
            file_list = u.read_models(folder, model_name)
        except:
            file_list = []
        initWindow["-FILE LIST-"].update(file_list)

    if event == "-FILE LIST-":
        pass

    ###############################################
    ##### ---------- BUTTON EVENTS ---------- #####
    ###############################################

    # Event for removing a model from the list
    if event == 'Remove':
        u.remove_model(file_list, values)
        initWindow["-FILE LIST-"].update(file_list)
        
    # Display Dataframe names in the dataframe box when hit the "make dataframe" button
    if event == 'Make Dataframe': 
        try:
            df, headers = setup.makeDataframe(file_list)
            if list(df.keys()) not in keys_list:
                df_list.append(df)
                keys_list.append(list(df.keys()))
        except NameError:
            pass
        
        initWindow["-DATAFRAME LIST-"].update(list(itertools.chain(*keys_list)))
        initWindow["-DATAFRAME LIST-"].values=list(itertools.chain(*keys_list))
        
        u.color_dataframe_sets(keys_list, initWindow["-DATAFRAME LIST-"]) # Color dataframes by set

    ###############################################
    ##### ---- CREATE DATAFRAMES WINDOW ----- #####
    ###############################################

    if event == 'Create Table':
        # Don't attempt to make tables if there are no dataframes
        if len(df_list) == 0:
            pass
        else:
            # Tried to save time by creating a cache of data tables.
            # In the end, the actual creation of the window is what takes the longest
            dataFrameWindow = setWin.make_dataframe_window(df_list, title="DataFrames")
            setWin.make_annotation_window(df_list)

    ###############################################
    ##### -------- DATAFRAMES EVENTS -------- #####
    ###############################################
    
    if event and "-DF TABLE-" in event:
        rowValues = []
        for row in values[event]:
            rowValues.append(dataFrameWindow[event].Values[row])

    ###############################################
    ##### ----- CREATE PLOTTING WINDOW ------ #####
    ###############################################

    if event == 'Plot':
        ''' Make new plotting window with options for making individual plots '''
        pass
        
