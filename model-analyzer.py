'''
Main script for the IMOD model analyzer GUI

@author: Matt Martinez
'''

import PySimpleGUI as sg
import os
import scripts.utils as util

# Create the window layout. Just one column might be necessary

file_selection_column = [
    [
        sg.Text("Enter common model name (or leave blank):"),
        sg.In(size=(25,1), enable_events=True ,key="-MODEL NAME-")
    ],
    [
        sg.Text("Select a folder:"),
        sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(button_text='Browse for parent folder', initial_folder='.')
    ],
    [
        sg.HSeparator()
    ]
]

file_list_column = [
    [
        sg.Listbox(values=[], enable_events=True, size=(40,20), key="-FILE LIST-", horizontal_scroll=True)
    ]
]

# ------- FULL LAYOUT ------- #

layout = [
    [
        sg.Column(file_selection_column)
    ],
    [
        sg.Push(), sg.Column(file_list_column, element_justification='c'), sg.Push()
    ],
    [
        sg.Push(), sg.Button('Remove'), sg.Push()
    ]
]

# Create the window and bind keys
window = sg.Window(title="IMOD Model Analyzer", layout=layout, finalize=True)
window["-MODEL NAME-"].bind("<Return>", "_Enter") # The keybind must be done after the window initialization is finalized

# Event loop
while True:
    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    # Get model name from the box
    if event == "-MODEL NAME-": 
        model_name = values["-MODEL NAME-"]
    elif event == "-MODEL NAME-" + "_Enter":
        # Get the model files from the given folder
        try:
            file_list = util.read_models(folder, model_name)
        except:
            file_list = []
        window["-FILE LIST-"].update(file_list)

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
            file_list = util.read_models(folder, model_name)
        except:
            file_list = []
        window["-FILE LIST-"].update(file_list)

    # Event for removing a model from the list
    if event == 'Remove':
        util.remove_model(file_list, values)
        window["-FILE LIST-"].update(file_list)
        
            
    if event == "-FILE LIST-":
        pass




window.close()