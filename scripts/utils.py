'''
Useful functions for the IMOD model analyzer

@author: Matt Martinez
'''

import PySimpleGUI as sg
import os

DEFAULT_WINDOW_SIZE = (867, 422)

def make_window(layout: list, title: str = None, size: tuple = DEFAULT_WINDOW_SIZE) -> sg.Window:
    return sg.Window(title=title, layout=layout, 
                     finalize=True, resizable=True, 
                     size=size)

def make_dataframe_window(df_list: list, title: str = None) -> sg.Window:
    '''
    Create a window with tabs, each containing a Pandas DataFrame
    Args: df_list - List containing groups of Pandas DataFrames
    '''

    layouts = {}
    for df in df_list:
        for key in df:
            pre_values = df[key].values.astype('object')
            pre_values[:,0:2] = pre_values[:,0:2].astype('int')
            values = pre_values.tolist()

            df_layout = [[
                sg.Table(values=values, headings=df[key].columns.tolist(),
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
    



def read_models(path, name=None) -> list:
    '''
    Read the filenames of all the specified model files.
    If given a specifc filename, use "find" from the specified directory.
    If not given a filenamr, just list all .mod files

    Return a list of file names

    Args: name - common string among the model files
    '''
    if not name: # If passed an empty string
        name = '*.mod'
    else:
        name = '*' + name + '*.mod'

    command = 'find ' + path + '/ -name "' + name + '"' 
    model_files = os.popen(command).read().rstrip('\n').split('\n') # rstip removes the final blank line from read()
    
    model_files = [os.path.join(path, f) for f in model_files if os.path.isfile(os.path.join(path, f)) and f.endswith(".mod")]

    return(model_files)

def remove_model(file_list, window_values) -> None:
    '''
    Remove a model from the file list if the user chooses to do so.
    
    Args: file_list - a list of file names
          window_valuse - values from window.read() 
    '''
    if len(file_list) > 0:
        try:
            val = window_values["-FILE LIST-"][0] # Gives the value of what's currently selected from the file list
            print(val)
            file_list.remove(val)
        except IndexError:
            pass

def color_dataframe_sets(keys: list, dataframes) -> None:
    '''
    Function to highlight Dataframes in the Dataframe window
    by model type. For example, you make a set of models on wildtype cells and
    a similar set of models on a mutant. Highlight the wildtype dataframes 
    one color,  and the mutant dataframes another.

    Args:   keys - 2D list of dataframe keys
            dataframes - Listbox object from window["-DATAFRAME LIST-"] 

    '''
    colors = ['skyblue', 'silver', 'mediumslateblue', 'yellow',
              'magenta', 'violet', 'slategray', 'sandybrown',
              'aqua', 'orchid', 'slateblue', 'lightgray']
    color_count = 0 # Track colors used
    index_count = 0 # Track items colored
    for model in keys:
        color = colors[color_count]
        for i in range(len(model)):
            dataframes.set_index_color(index_count, 'white', color)
            index_count += 1
        color_count += 1
    
def test_read_models():
    read_models('/ChangLab1-hd3/matt/Toxoplasma/ROPx','MV_model')

if __name__ == '__main__':
    test_read_models()