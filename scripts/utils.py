'''
Useful functions for the IMOD model analyzer

@author: Matt Martinez
'''

import PySimpleGUI as sg
import pandas as pd
import os
import csv

TABLE_PATH = f'{os.path.realpath(os.path.dirname(__file__))}/../.data/__table_cache__/'

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


def write_table(key: str, headers: list[str], values: list) -> None:
    ''' 
    Write the PySimpleGUI tables to CSV files

    Args:
        key (str): The key used to generate the filename
        headers (list[str]): The list of column headers
        values (list): The list of rows with values 
    '''

    basename = key.replace('.txt', '')
    with open(f'{TABLE_PATH}{basename}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)  # Write the headings
        writer.writerows(values)  # Write the values


def read_table(key: str) -> [list[str], list]:
    ''' 
    Read the PySimpleGUI tables from CSV files
    Args:
        key (str): The key used to generate the filename

    Return:
        headers (list[str]): The list of column headers
        values (list): The list of rows with values
    '''
    basename = key.replace('.txt', '')
    if not basename.endswith('.csv'):
        basename = f'{basename}.csv'

    # Check if file exists
    if not os.path.isfile(f'{TABLE_PATH}{basename}'):
        # File does not exist
        return

    with open(f'{TABLE_PATH}{basename}', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        values = list(reader)

    return headers, values


def read_cached_tables():
    ''' 
    Read in all the cached tables 
    Returns a dictionary of tables by model
    '''

    files = os.listdir(TABLE_PATH)
    tables = dict()

    for file in files:
        if file.endswith('.csv'):
            key = file.split('.')[0]
            tables[key] = read_table(file)

    return tables

def test_read_models():
    read_models('/ChangLab1-hd3/matt/Toxoplasma/ROPx','MV_model')


if __name__ == '__main__':
    test_read_models()