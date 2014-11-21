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
    products = df_data.columns.values.tolist()
    df_data[products]=df_data[products].astype(float)
    regions = df_data.index.astype(str)
    return df_data, products, regions

def case_generator(regions, pcases):
    return vose.Vose(zip(regions,pcases))

def cases (case_gen, nocases):
    c = [case_gen.get() for i in range(nocases)]
    return Counter(c)

def foodConsumption(regions, product):
    return dict(zip(regions, product))

def likelihood(cas, fc):
    l=list()
    for region in cas.iterkeys():
        x = cas.get(region)
        p = fc.get(region)
        if p > 0:
            l.append(x*np.log10(p))
    return(np.sum(l))

def simulate(cl, ch, rep, f_out):
    df_data, P, R = readdata()

    #
    # open file for writing
    f = open(f_out,'w')
    for nocases in np.arange(cl,ch,1):
        for tp in P:
            cg = case_generator(R, df_data[tp].tolist())
            for r in range(rep):
                scases = cases(cg,nocases)
                for p in P:
                    fc = foodConsumption(R, df_data[p].tolist())
                    likely = likelihood(scases,fc)
                    #print nocases, tp.replace("Product ",""), p.replace("Product ",""), r, likely
                    f.write('%s,%s,%s,%d,%f\n' % (nocases, 
                                                  tp.replace("Product ",""), 
                                                    p.replace("Product ",""), 
                                                    r, likely))
    f.close()

def main(argv):
    noc = ''
    N    = ''
    f_out = ''
    try:
        opts,_ = getopt.getopt(argv,"hc:N:o:")
    except getopt.GetoptError:
        print 'AFD.py -c <cases> -N <no replicates> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'AFD.py -c <cases> -N <no replicates> -o <outputfile>'
            sys.exit()
        elif opt == '-c':
            noc = arg
        elif opt == '-N':
            N = arg
        elif opt == '-o':
            f_out = arg

    print 'Cases      : ', noc
    print 'Replicates : ', N
    print 'output file: ', f_out

    simulate(int(noc), int(noc)+1, int(N), f_out)

#
# This is the entry point
#
if __name__ == '__main__':
    #
    # read comand line parameters
    main(sys.argv[1:])



