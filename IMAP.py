# -*- coding: utf-8 -*-
"""
ImageMap.py
Image Map of food sales
Created on Thu Oct 30 09:46:30 2014

@author: TOSS
"""
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np

im = np.arange(100)
im.shape = 10,10

fig = plt.figure(1,(4.,4.))
grid = ImageGrid(fig, 111, nrows_ncols = (2,2), axes_pad=0.1)

for i in range(4):
    grid[i].imshow(im)
    
plt.show()

