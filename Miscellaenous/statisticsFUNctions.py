import time
import os
import math
import pyodbc


def levelComparisons():
    levelList = ['L1','L2','L3','L4','L5','L6']
    compareList = []
    levels = len(levelList)

    for x in range(0,levels):
        y = x+1
        for y in range(y ,levels):
            try:
                compareList.append([levelList[x],levelList[y]])
            except IndexError:
                pass
    print('Levels:',levelList)
    print('Comparisons:',compareList)
    print('Number of Comparisons:',len(compareList))

    
if __name__ == "__main__":
    levelComparisons()