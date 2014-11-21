# -*- coding: utf-8 -*-
"""
Spyder Editor

FileName CaseSoources.py
date 10.11.2014
Description:
The program assesses the identification of sources of simulated cases on the 
basis of food product consumption. Additional a proportion of p cases are 
generated form other reasons
"""

import numpy as np
import vose
from collections import Counter

#
# read the sales data skip first col and first row
with open('./Daten/Dataset_S1.csv') as f:
    ncolsdata = len(f.readline().split(','))
print 'Cols in data ', ncolsdata
data = np.loadtxt(open('./Daten/Dataset_S1.csv','rb'),delimiter=',',skiprows=1, 
                  usecols = range(1,ncolsdata))
rows,cols = data.shape
# this will be the number of replicates per product
CaseMat = np.zeros((cols,rows), dtype=int)
print 'Shape of CaseMat is: ', CaseMat.shape
print 'This is first col of data'
print data[:,0]

#
# create Cases cases
Cases = 100
#noCols2Consider=ncolsdata
noCols2Consider = 3
x = np.arange(rows)
#for c in range(1,cols-1):
print 'I am generating the cases'
for c in range(noCols2Consider-1):
    print 'looking at col', c
    CaseGenerator = vose.Vose(zip(x,data[:,c]))
    CaseList = [CaseGenerator.get() for _ in range(Cases)]
    CaseFreq = Counter(CaseList)
    for f in CaseFreq.iterkeys():
        CaseMat[c,f]=CaseFreq.get(f)

#
# get the sum and max of cases in caseMat
for c in range(noCols2Consider-1):
    print c, CaseMat[c].sum(), CaseMat[c].max()
    
#
# print casemat
print CaseMat[:2,:]

#
# reduce CaseMat to first two cols and transponse
np.savetxt('FeatureMatrix.csv', CaseMat[:2,:], delimiter=',', fmt='%d')
