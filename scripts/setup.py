'''
Setup functions for the IMOD models into a Pandas dataframe.

@author: Matt Martinez
'''

import subprocess
import os.path
import pandas as pd

def model2point(file_list: list) -> list:
    
    '''
    Utilize the PEET command, model2point, to convert
    desired model files into xyz point files. Store those files
    in a temporary directory

    Return list for the dataframe

    Args: file_list - list of file names
    '''
    new_file_list = []
    for file in file_list:
        file_prefix = file.split('/')[:-1]
        file_prefix.pop(0)

        # Create new file path and name
        name = ''
        for item in file_prefix:
            name += item + '_'

        file_path = os.path.realpath(os.path.dirname(__file__)) + '/../__model_cache__/'
        file_name = name + file.split('/')[-1].split('.')[0] + '.txt' 

        # Run model2point on the models, if the text files don't already exit
        if not os.path.isfile(f'{file_path}{file_name}'):
            process = subprocess.run(['model2point', '-ob', f'{file}', f'{file_path}{file_name}'])
        
        new_file_list.append(f'{file_path}{file_name}')

    return new_file_list

def makeDataframe(file_list: list) -> dict:

    '''
    From the IMOD models converted to text files, create
    a Pandas dataframe for viewing

    Return the dataframe

    Args: file_list - list of .txt files
    '''

    models_dataFrame = dict()

    # Read all text files into a list
    files = model2point(file_list)

    # Read in data points from the files and assemble into dataframe
    for file in files:
        with open(file, 'r') as f:
            points = f.readlines()
        points = [line.strip().split() for line in points]

        #Convert points into a Pandas dataframe
        df = pd.DataFrame({'Ob':[int(points[0][0])], 'Ct':[int(points[0][1])],
                           'X':[float(points[0][2])], 'Y':[float(points[0][3])], 'Z':[float(points[0][4])]})
        count = 1 
        for line in points[1:]:
            df = df.append(pd.DataFrame({'Ob':[int(points[count][0])], 'Ct':[int(points[count][1])],
                                         'X':[float(points[count][2])], 'Y':[float(points[count][3])], 'Z':[float(points[count][4])]}),
                                         ignore_index=True)
            count += 1

        models_dataFrame[file.split('/')[-1]] = df
    return models_dataFrame



def test_model2point():
    model2point(['/ChangLab1-hd3/matt/GUI_IMOD_models/test_models/MV_model.mod'])

def test_makeDateframe():
    makeDataframe(['/ChangLab1-hd3/matt/GUI_IMOD_models/test_models/MV_model.mod',
                   '/ChangLab1-hd3/matt/GUI_IMOD_models/test_models/MV_model2.mod',
                   '/ChangLab1-hd3/matt/GUI_IMOD_models/test_models/MV_model3.mod',
                   '/ChangLab1-hd3/matt/GUI_IMOD_models/test_models/MV_model4.mod'])
    
def test_printcwd():
    print(os.path.realpath(os.path.dirname(__file__)) + '/../__model_cache__/')

if __name__ == '__main__':
    test_makeDateframe()