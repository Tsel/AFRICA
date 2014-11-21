# coding: utf-8

# #Simulate and assess foodborn cases


import sys, getopt
import pandas as pd
import vose
import numpy as np
from collections import Counter



def readdata():
    f_data = "Dataset_S1.csv"
    df_data = pd.read_csv(f_data, index_col=0)
    products = list(df_data.columns.values)
    df_data[products]=df_data[products].astype(float)
    regions = df_data.index.astype(str)
    return df_data, products, regions

def case_generator(regions, pcases):
    return vose.Vose(zip(regions,pcases))

def cases (case_gen, nocases):
    c = [case_gen.get() for i in range(nocases)]
    return Counter(c)

def foodConsumption(regions, product):
    return dict(zip(regions,product))

def likelihood(cases,fc):
    l=list() 
    for region in cases.iterkeys():
        x = cases.get(region)
        p = fc.get(region)
        if p > 0:
            l.append(x*np.log10(p))
    return(np.sum(l))

#rep     = 2  # number of times the simulation experiment is repeated
#nocases = 10    # number of cases simulated to be set on command line
#for true_product in products[:2]:
    
#    cg = case_generator(regions,df_data[true_product].tolist())
#    for r in range(rep):
        #
        # Cases generation for product 'true_product'
#        scases = cases(cg,nocases)
        #print scases
        #
        # compare cases with consumption of product p
#        for prod in products:
#            fc = foodConsumption(regions,df_data[prod].tolist())
#            likely = likelihood(scases,fc)
            #
            # output
#            print nocases, true_product, prod, r, likely
            
def simulate(cl, ch, rep, f_out):
    df_data, R, P = readdata()
    
    for nocases in np.arange(cl,ch,1):
        for tp in P:
            cg = case_generator(R, df_data[tp].tolist())
            for r in range(rep):
                scases = cases(cg,nocases)
                for p in P:
                    fc = foodConsumption(R, df_data[p].tolist())
                    likely = likelihood(scases,fc)
                    print nocases, tp, p, r, likely
                
def main(argv):
    nocl = ''
    noch = ''
    N    = ''
    f_out = ''
    try:
        opts, args = getopt.getopt(argv,"hl:h:N:o:")
    except getopt.GetoptError:
        print 'AFD.py -l <cases low> -h <cases high> -N <no replicates> -o <outputfile>'
    for opt, arg in opts:
        if opt == '-h':
            print 'AFD.py -l <cases low> -h <cases high> -N <no replicates> -o <outputfile>'
            sys.exit()
        elif opt == '-l':
            nocl = arg
        elif opt == '-h':
            noch = arg
        elif opt == '-N':
            N = arg
        elif opt == '-o':
            f_out = arg
            
    print 'Cases from : ', nocl
    print 'Cases to   : ', noch
    print 'Replicates : ', N
    print 'output file: ', f_out
    
    simulate(int(nocl), int(noch), int(N), f_out)
        
#
# This is the entry point
#
if __name__ == '__main__':
    #
    # read comand line parameters
    main(sys.argv[1:])
    


