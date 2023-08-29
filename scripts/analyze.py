'''
Analysis functions for the IMOD model analyzer GUI.

Functions include creating and displaying Pandas datafranes
and simple calculations

@author: Matt Martinez
'''

import os
import numpy as np
import math

def model2point(file_list):
    '''
    Utilize the PEET command, model2point, to convert
    desired model files into xyz point files. Store those files
    in a temporary directory

    Return nothing

    Args: file_list - list of file names
    '''
    commands = [] # List of commands to execute
    for file in file_list:
        file_prefix = file.split('/')[:-1]
        file_prefix.pop(0)

        # Create prefix for output file name
        name = ''
        for item in file_prefix:
            name += item + '_'

        file_name = file.split('/')[-1].split('.')[0]
        command = f"model2point {file_name}.mod __model_cache__/{name+file_name}.txt"

        print(name)
        print(command)

# Two functions to calculate distances between points
def calcDist(a,b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

def calcTotalDist(a):
    cumDist = 0
    for i in range(len(a)-1):
        dist = calcDist(a[i],a[i+1])
        cumDist += dist
    return cumDist

def test_model2point():
    model2point(['/ChangLab1-hd2/matt/model1.mod','/ChangLab1-hd2/matt/model2.mod','/ChangLab1-hd2/matt/model3.mod'])

if __name__ == '__main__':
    test_model2point()