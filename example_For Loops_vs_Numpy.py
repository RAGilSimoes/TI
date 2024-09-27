#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:59:36 2024

@author: rpp
"""

import matplotlib.pyplot as plt
import numpy as np
import time


def showimg(img):
    plt.figure()
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    


def main():
    plt.close('all')
    
    #---- read img
    fName = "polarbear.jpg"   #"image008.jpg"
    img = plt.imread(fName)  #matplotlib.img.imread
    
    #---- show img
    showimg(img)
    
    nRep = 1  #number of repetitions of image rostart = time.time()tation
    
    #--- rotate image (transpose)
    start = time.time()
    for rep in range(nRep):
        imgRT = img.transpose((1, 0, 2))
    end = time.time()
    print("Time using numpy: %.5f seconds." % (end - start))
    showimg(imgRT)
    
    #--- rotate image (loops)
    start2 = time.time()
    for rep in range(nRep):
        nl, nc, nCh = img.shape
        imgRC = np.empty((nc, nl, nCh), dtype = np.uint8)
        for k in range(nCh):
            for i in range(nc):
                for j in range(nl):
                    imgRC[i, j, k] = img[j, i, k]
    end2 = time.time()
    print("Time using for loops: %.5f seconds." % (end2 - start2))
    showimg(imgRC)
     

if __name__ == "__main__":
    main()
