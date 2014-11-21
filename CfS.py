# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 14:34:29 2014
create cases from food sources
@author: TOSS
"""

import numpy as np
import vose
from collections import Counter
#
# read the sales data skip first col and first row
with open('../Daten/Dataset_S1.csv') as f:
    ncolsdata = len(f.readline().split(','))
print 'Cols in data ', ncolsdata
#~/Documents/Projects/FoodContamination/Daten/Dataset_S1.csv
data = np.loadtxt(open('../Daten/Dataset_S1.csv','rb'),delimiter=',',skiprows=1, 
                  usecols = range(1,ncolsdata))
regions,prods = data.shape
#
# Array to hold the number of cases
CaseVec = np.zeros(regions, dtype=int)

#
# generate the cases
Cases = 100
noCols2Consider = 13
# repetitions
rep=900
blur = 0.01
#
# CaseMat considering noCols2Consider and reps will have 
# noCols2Consider x rep rows
cm_rows = noCols2Consider*rep
CaseMat = np.zeros((cm_rows,regions), dtype=int)
x = np.arange(regions)
#for c in range(1,cols-1):
counter=0
print 'I am generating the cases'
for c in np.arange(noCols2Consider):
    data[:,c] = data[:,c]*(1-blur)+blur
    data[:,c] = data[:,c] / np.sum(data[:,c])
    CaseGenerator = vose.Vose(zip(x,data[:,c]))
#    print 'looking at product', c
    for _ in range(rep):
        #print 'looking at col', c
        CaseList = [CaseGenerator.get() for _ in range(Cases)]
        CaseFreq = Counter(CaseList)
        for f in CaseFreq.iterkeys():
            CaseMat[counter,f]=CaseFreq.get(f)
        
        #print CaseMat[counter].sum(), CaseMat[counter].max()
        counter += 1
    
print CaseMat.shape
print CaseMat


#
# save features to file
np.savetxt('../Daten/FeatureMatrixC100.csv', CaseMat, delimiter=',', fmt='%d')
#
# create and save the targets
np.savetxt('../Daten/TargetVectorC100.csv', np.repeat(np.arange(noCols2Consider),rep), fmt='%d')

