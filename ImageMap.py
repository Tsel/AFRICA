# -*- coding: utf-8 -*-
"""
ImageMap.py
Image Map of food sales
Created on Thu Oct 30 09:54:43 2014

@author: TOSS
"""
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np
import pandas as pd

df = pd.read_csv('/Users/TOSS/Documents/Projects/FoodContamination/Dataset_S1.csv', index_col=0)
prods = list(df.columns.values)

fig = plt.figure(1,(60.0,36.0))
grid = ImageGrid(fig,111,nrows_ncols=(29,20),axes_pad=0.01,share_all=True,label_mode='1')

counter=0
for i in range(580):
    p = prods[i]
    p0 = df[p].values
    p0 = np.append(p0,0.)
    p0 = p0.reshape(69,51)
    grid[counter].imshow(p0, interpolation='nearest')
    counter += 1
    
plt.show()

from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('ImageMap.pdf')
pp.savefig(fig)
pp.close()
    
