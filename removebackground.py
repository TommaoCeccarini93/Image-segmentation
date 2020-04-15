# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 14:42:16 2020

@author: Tommaso
"""

import os
from activecontour import removeBackground
from time import time

def loadImagesFromFolder(readFolder,alpha=0.015,beta=10,size=1000,w=2600,h=1733):
    writeFolder = readFolder+'-no-background'
    os.makedirs(writeFolder)
    for filename in os.listdir(readFolder):
        print("Remove background from image {filename}.".format(filename=filename))
        t1 = time()
        removeBackground(filename,readFolder,writeFolder,alpha,beta,size,w,h)
        t2 = time()
        elapsed = t2-t1
        print("Remove background from image {filename} took {elapsed} seconds.".format(filename=filename,elapsed=elapsed))
    