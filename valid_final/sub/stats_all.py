#! /usr/bin/env python
#-*- coding: utf-8 -*-
#2/2019, Olga Vähä-Piikkiö



import numpy as np
import matplotlib
matplotlib.use('Agg') # ensure that X11 is not used, this script is intended for server use
import matplotlib.pyplot as plt
import subprocess

from scipy.io import netcdf
import scipy
import os
import math
import matplotlib as mpl
import sys



arraypath=sys.argv[2]



for j in [sys.argv[1]]:
    fwdat2_wh=np.empty([0])  
    fwdat6_wh=np.empty([0])  

    for w in sys.argv[3:]:

        tname=''.join(c for c in str(w) if c.isalpha())


        dat2=np.load(''+arraypath+'b_'+j+'_'+tname+'.npy')
        dat6=np.load(''+arraypath+'w_'+j+'_'+tname+'.npy')


        fwdat2_wh=np.hstack([fwdat2_wh, dat2])
        fwdat6_wh=np.hstack([fwdat6_wh, dat6])



#calculating and printing statistics


    hs2m=np.mean(fwdat2_wh, dtype=np.float64)

    hs6m=np.mean(fwdat6_wh, dtype=np.float64)


    aaa=0
    aaa2=0
    aaa3=0
    aaa4=0
    aaa5=0



    www=0


    aaa=0
    aaa2=0
    aaa3=0
    aaa4=0
    aaa5=0
    aaa6=0
    b_cov=0
    w_cov=0
    for aaaa, bbbb in zip(fwdat2_wh, fwdat6_wh):
        aaa=aaa+(bbbb-aaaa)
        aaa6=aaa6+abs((aaaa-bbbb))
        aaa2=aaa2+math.pow(bbbb-aaaa,2)
        aaa3=aaa3+(aaaa-hs2m)*(bbbb-hs6m)
        aaa4=aaa4+math.pow(aaaa-hs2m,2)
        aaa5=aaa5+math.pow(bbbb-hs6m,2)
        b_cov=b_cov+(aaaa-hs2m)
        w_cov=w_cov+(bbbb-hs6m)




    var_b=float(aaa4)/float(len(fwdat2_wh))
    var_w=float(aaa5)/float(len(fwdat2_wh))

    std_b=math.sqrt(float(aaa4)/float(len(fwdat2_wh)))
    std_w=math.sqrt(float(aaa5)/float(len(fwdat2_wh)))



    bias_hs=float(aaa)/float(len(fwdat2_wh))
    sterror_hs=float(aaa6)/float(len(fwdat2_wh))
    rmse_hs=math.sqrt(float(aaa2)/float(len(fwdat2_wh)))
    mse=float(aaa2)/float(len(fwdat2_wh))


    corr_hs=float(aaa3)/float(math.sqrt(aaa4*aaa5))

    cov=float(aaa3)/float(len(fwdat2_wh))


    SI=rmse_hs/hs2m

  

    print'\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!'

    print j
    print '!!!!!!!!!!!!!!!!!!!!!'

    print 'mean_buoy'
    print hs2m
    print '\n mean_wam'
    print hs6m
    print '\nvar_buoy'
    print var_b
    print '\nvar_wam'
    print var_w
    print '\nstd_buoy'
    print std_b
    print '\nstd_wam'
    print std_w             

    print '\ncov'
    print cov

    print '\nMSE'
    print mse


    print '\nRMSE'
    print rmse_hs

    print '\nCORR'
    print corr_hs
 
    print '\nBIAS'
    print bias_hs

    print '\nMAE'
    print sterror_hs

    print '\nSI'
    print SI








