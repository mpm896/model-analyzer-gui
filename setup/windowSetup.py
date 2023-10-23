import PySimpleGUI as sg
import scripts.utils as u
import time

DEFAULT_WINDOW_SIZE = (867, 422)
THEME = 'Black2'


def make_window(layout: list, title: str = None, size: tuple = DEFAULT_WINDOW_SIZE, theme=THEME) -> sg.Window:
    return sg.Window(title=title, layout=layout, 
                     finalize=True, resizable=True, 
                     size=size)

def make_dataframe_window(df_list: list, title: str = None) -> sg.Window:
    '''
    Create a window with tabs, each containing a Pandas DataFrame
    Args: 
        df_list (list): List containing groups of Pandas DataFrames
    '''
    sg.theme(THEME)
    layouts = {}

    for df in df_list:
        for key in df:
            try:
                header, values = u.read_table(key)
            except TypeError:
                header = df[key].columns.tolist()
                values = df[key].values.astype('object')
                values[:,0:2] = values[:,0:2].astype('int')
                values = values.tolist()

                # Write the headings and values to a csv file
                u.write_table(key, df[key].columns.tolist(), values)
                
            df_layout = [[
                sg.Table(values=values, headings=header,
                        key=f"-DF TABLE-", enable_events=True,
                        expand_x=True, expand_y=True,
                        select_mode='extended')
            ]]
            layouts[key] = df_layout

    tabgroup = [[sg.Tab(key, layouts[key], key=key, tooltip=f'{key}') for key in layouts]]
    
    tableLayout = [[
            sg.TabGroup(tabgroup, key='TabGroup', 
                        expand_x=True, expand_y=True,
                        enable_events=True)
        ]]
    
    return make_window(tableLayout, title=title)


def make_annotation_window(df_list: list, title: str=None) -> sg.Window:
    ''' Window for annotating model objects. Allow user to input annotation once if all are the same,
        or input object annotations model by model  '''
    objects = dict()  # Keep track of objects for use, if they want to annotate all at once or for each model
    max = 0
    for df in df_list:
        name = list(df.keys())[0]
        df = list(df.values())[0]  # Get dataframe object
        num_objects = df['Ob'].unique()
        if (len_objects := num_objects) > max:
            max = len_objects

        objects[name] = num_objects
    ### Add a loop to create a column for the number of objects, with an input box for each object ###
    layout = [[sg.Push(), sg.Radio("Annotate all models", default=True), sg.Push()]
              [sg.Push()]] # Filler column with the push object

def make_plotting_window(df_list: list, title: str=None) -> sg.Window:
    '''
    Make a window giving the user options for plotting their 
    data from the dataframes
    '''
    pass