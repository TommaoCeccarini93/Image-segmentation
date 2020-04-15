# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 19:34:20 2020

@author: Tommaso
"""

import numpy as np
import numpy.ma as ma
from skimage.color import rgb2gray
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage.draw import polygon
import cv2
from PIL import Image
import piexif

def removeBackground(imagename,readFolder,writeFolder,alpha,beta,size,w_res,h_res):
    #Use PIL and piexif to save exif data
    im = Image.open(readFolder+'/'+imagename)
    exif_dict = piexif.load(im.info["exif"])
    exif_bytes = piexif.dump(exif_dict)
    
    image = cv2.imread(readFolder+'/'+imagename)
    image = cv2.resize(image,(w_res,h_res))
    img = image.copy()
    img = rgb2gray(img)

    #initial contour (ellipse)
    s = np.linspace(0, 2*np.pi, size)
    r = 840 + 850*np.sin(s)
    c = 1250 + 750*np.cos(s)

    init = np.array([r, c]).T

    snake = active_contour(gaussian(img, 3),init, alpha=alpha, beta=beta, gamma=0.001,coordinates='rc')
    
    mask = np.zeros(img.shape)
    rr,cc = polygon(snake[:,0],snake[:,1],mask.shape)
    mask[rr,cc] = 1
    masked = ma.array(img.copy(),mask=mask)
    m = masked.data*masked.mask

    masked_image = np.zeros((h_res,w_res,3))
    masked_image[:,:,0] = image[:,:,0]*m
    masked_image[:,:,1] = image[:,:,1]*m
    masked_image[:,:,2] = image[:,:,2]*m

    cv2.imwrite(writeFolder+'/'+imagename,masked_image,[cv2.IMWRITE_JPEG_QUALITY, 100])
    
    #add the exif data of the original image to the image without background
    im = Image.open(writeFolder+'/'+imagename)
    im.save(writeFolder+'/'+imagename,"JPEG",quality=100,exif=exif_bytes)

