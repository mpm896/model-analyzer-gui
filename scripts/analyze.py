'''
Analysis functions for the IMOD model analyzer GUI.

Functions include creating and displaying Pandas datafranes
and simple calculations

@author: Matt Martinez
'''

import os
import numpy as np
import math

# Two functions to calculate distances between points
def calcDist(a,b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

def calcTotalDist(a):
    cumDist = 0
    for i in range(len(a)-1):
        dist = calcDist(a[i],a[i+1])
        cumDist += dist
    return cumDist

if __name__ == '__main__':
    pass