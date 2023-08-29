'''
Main script for the IMOD model analyzer GUI

@author: Matt Martinez
'''

import PySimpleGUI as sg
import os
import scripts.utils as u
import scripts.setup as setup
import scripts.analyze as a


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
    ]
]

file_list_column = [
    [
        sg.Listbox(values=[], enable_events=True, size=(40,20), key="-FILE LIST-", horizontal_scroll=True),
        sg.Button(button_text='Make Dataframe', size=(9,2))
    ],
    [
        sg.Button('Remove')
    ]
]

dataframe_list_column = [
    [
        sg.Text("Dataframes", font=(None, 15, 'underline'))
    ],
    [
        sg.Listbox(values=[], enable_events=True, size=(30,15), key="-DATAFRAME LIST-", horizontal_scroll=True)
    ]
]

# ------- FULL LAYOUT ------- #

layout = [

    [
        sg.Push(), sg.Column(file_selection_column), sg.Push()
    ],
    [
        sg.HSeparator()
    ],
    [
        sg.Column(file_list_column, element_justification='c'),
        sg.VSeparator(),
        sg.VPush(), sg.Column(dataframe_list_column, element_justification='c'), sg.VPush()
    ]
]

# Create the window and bind keys
window = sg.Window(title="IMOD Model Analyzer", layout=layout, finalize=True)
window["-MODEL NAME-"].bind("<Return>", "_Enter") # The keybind must be done after the window initialization is finalized

# Initialize the dataframes
df_list = []

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
            file_list = u.read_models(folder, model_name)
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
            file_list = u.read_models(folder, model_name)
        except:
            file_list = []
        window["-FILE LIST-"].update(file_list)


    # Event for removing a model from the list
    if event == 'Remove':
        u.remove_model(file_list, values)
        window["-FILE LIST-"].update(file_list)
        
    # Display Dataframe names in the dataframe box when hit the "make dataframe" button
    if event == 'Make Dataframe':
        try:
            if setup.makeDataframe(file_list) not in df_list:
                df_list.append(setup.makeDataframe(file_list))
        except NameError:
            pass
        
            
    if event == "-FILE LIST-":
        pass


window.close()