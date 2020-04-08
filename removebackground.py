# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 14:42:16 2020

@author: Tommaso
"""

import os
from activecontour import removeBackground
from time import time

def loadImagesFromFolder(readFolder):
    writeFolder = readFolder+'-no-background'
    os.makedirs(writeFolder)
    for filename in os.listdir(readFolder):
        print("Remove background from image {filename}.".format(filename=filename))
        t1 = time()
        removeBackground(filename,readFolder,writeFolder)
        t2 = time()
        elapsed = t2-t1
        print("Remove background from image {filename} took {elapsed} seconds.".format(filename=filename,elapsed=elapsed))
    