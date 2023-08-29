'''
Useful functions for the IMOD model analyzer

@author: Matt Martinez
'''

import os

def read_models(path, name=None):
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

def remove_model(file_list, window_values):
    '''
    Remove a model from the file list if the user chooses to do so.
    Return a modified list of file names
    Args: file_list - a list of file names
          window_valuse - values from window.read() 
    '''
    if len(file_list) > 0:
        val = window_values["-FILE LIST-"][0] # Gives the value of what's currently selected from the file list
        file_list.remove(val)
    
def test_read_models():
    read_models('/ChangLab1-hd3/matt/Toxoplasma/ROPx','MV_model')

if __name__ == '__main__':
    test_read_models()