import PySimpleGUI as sg

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
        sg.Button('Remove'), sg.Push()
    ]
]

dataframe_list_column = [
    [
        sg.Text("Dataframes", font=(None, 15, 'underline'))
    ],
    [
        sg.Listbox(values=[], enable_events=True, size=(30,15), key="-DATAFRAME LIST-", horizontal_scroll=True)
    ],
    [
        sg.Push(), sg.Button('Create Table'), sg.Push()
    ]
]

# ------- FULL LAYOUT ------- #

def get_initial_layout() -> list:
    return [
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

