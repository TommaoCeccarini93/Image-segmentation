# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:47:30 2020

@author: Tommaso
"""

from removebackground import loadImagesFromFolder

#remove background from skull-turntable
loadImagesFromFolder('skull-turntable')

#remove background from skull-turntable-shallow-dof
loadImagesFromFolder('skull-turntable-shallow-dof',alpha=0.003,size=1500)