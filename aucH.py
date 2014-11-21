
# -*- coding: utf-8 -*-

import numpy as np


def exact_CI(x, N, alpha=0.95):
    """
    Calculate the exact confidence interval of a proportion 
    where there is a wide range in the sample size or the proportion.

    This method avoids the assumption that data are normally distributed. The sample size
    and proportion are desctibed by a beta distribution.

    Parameters
    ----------

    x: the number of cases from which the proportion is calulated as a positive integer.

    N: the sample size as a positive integer.

    alpha : set at 0.95 for 95% confidence intervals.

    Returns
    -------
    The proportion with the lower and upper confidence intervals as a dict.

    """
    from scipy.stats import beta
    x = float(x)
    N = float(N)
    p = round((x/N)*100,2)

    intervals = [round(i,4)*100 for i in beta.interval(alpha,x,N-x+1)]
    intervals.insert(0,p)

    return intervals[1]/100., intervals[2]/100.

def auc_H(va,vn):
    """
    Calculates the area under ROC cuve according to the paper of J. Hanley and B.J. McNeil (1982). The meaning and Use of the Area under a Receiver Opearting Characteristic (ROC) Curve. Radiology, Vol 143, No. 1 pp 29-36.
    
    The calculation is slightely altered in order to test for the largest differences between va and vn.
    
    Parameters
    ----------
    va: Measurements for group 0
    vn: Measurements for group 1
    
    Returns
    -------
    auc: area under roc cuve
    se : estimated standard error
    ll : lower limit of confidence interval
    ul : upper limit of confidence interval
    
    """
    na = len(va)
    nn = len(vn)
    #
    # calculate the auc
    s_pos   = list() 
    s_split = list() 
    s_neg   = list()
    for i in va:
        for j in vn:
            if(j>i):
                s_pos.append(1.)
            elif(j==i):
                s_split.append(0.5)
            else:
                s_neg.append(1.0)
    
    auc = (np.maximum(np.sum(s_pos),np.sum(s_neg)) + np.sum(s_split)) / (na*nn)
    #
    # determine standard errror
    Q1 = auc/(2.-auc)
    Q2 = 2*np.square(auc)/(1.+auc)
    d1 = auc*(1.-auc)
    d2 = (na-1.)*(Q1-np.square(auc))
    d3 = (nn-1.)*(Q2-np.square(auc))
    
    se = np.sqrt((d1+d2+d3)/(na*nn))
    
    N = int(na+nn)
    x = int(auc*N)
    
    
    return auc, se, exact_CI(x,N) 

