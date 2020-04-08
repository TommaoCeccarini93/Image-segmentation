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

def removeBackground(imagename,readFolder,writeFolder,w_res=2600,h_res=1733):
    #Uso PIL e piexif per salvare gli Exif data
    im = Image.open(readFolder+'/'+imagename)
    exif_dict = piexif.load(im.info["exif"])
    exif_bytes = piexif.dump(exif_dict)
    
    image = cv2.imread(readFolder+'/'+imagename)
    image = cv2.resize(image,(w_res,h_res))
    img = image.copy()
    img = rgb2gray(img)
    #img = cv2.resize(img,(2600,1733))

    #initial contour (ellipse)
    s = np.linspace(0, 2*np.pi, 1000)
    r = 840 + 850*np.sin(s)
    c = 1250 + 750*np.cos(s)

    init = np.array([r, c]).T

    snake = active_contour(gaussian(img, 3),init, alpha=0.015, beta=10, gamma=0.001,coordinates='rc')
    
    """"
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(img, cmap=plt.cm.gray)
    ax.plot(init[:, 1], init[:, 0], '--r', lw=3)
    ax.plot(snake[:, 1], snake[:, 0], '-b', lw=3)
    ax.set_xticks([]), ax.set_yticks([])
    ax.axis([0, img.shape[1], img.shape[0], 0])

    plt.show()
    """
    
    mask = np.zeros(img.shape)
    rr,cc = polygon(snake[:,0],snake[:,1],mask.shape)
    mask[rr,cc] = 1
    #mask = 1 - mask
    masked = ma.array(img.copy(),mask=mask)
    m = masked.data*masked.mask

    masked_image = np.zeros((h_res,w_res,3))
    masked_image[:,:,0] = image[:,:,0]*m
    masked_image[:,:,1] = image[:,:,1]*m
    masked_image[:,:,2] = image[:,:,2]*m

    cv2.imwrite(writeFolder+'/'+imagename,masked_image,[cv2.IMWRITE_JPEG_QUALITY, 100])
    
    #aggiungo gli exif data dell'immagine originale all'immagine senza background
    im = Image.open(writeFolder+'/'+imagename)
    im.save(writeFolder+'/'+imagename,"JPEG",quality=100,exif=exif_bytes)

