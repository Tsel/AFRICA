# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 09:28:33 2014
SVM4FoodCases
@author: TOSS
"""
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import train_test_split
import numpy as np

import matplotlib.pyplot as plt
#
# load the data
X = np.loadtxt('../Daten/FeatureMatrixC100.csv', dtype=int, delimiter=',')
y = np.loadtxt('../Daten/TargetVectorC100.csv', dtype=int, delimiter=',')

print X.shape, y.shape

#
# split data into training and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

#
# setup
svc = svm.SVC(kernel='linear', C=1.0).fit(X_train, y_train)
#
# prediction from original data
y_pred = svc.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

print cm
t = np.trace(cm)
s = np.sum(cm)
print t, s, float(t)/float(s)


#plt.matshow(cm)
#plt.title('Confusion matrix')
#plt.colorbar()
#plt.ylabel('True label')
#plt.xlabel('Predicted label')
#plt.show()