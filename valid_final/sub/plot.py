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
import matplotlib.dates as mdates
import sys
import datetime
import matplotlib.ticker as ticker


prefix=sys.argv[2]
plotfix=sys.argv[3]

buoypath=sys.argv[6]

arraypath=sys.argv[7]

saveplotpathL=sys.argv[5]


vari=sys.argv[4] 
for v in [sys.argv[1]]:

    tname=v    
#    tname=w[:-3]
#    tname=tname[9:]
    print tname
    print arraypath
    

#    muut=['wheight', 'pperiod']


#    for j in muut:

   
    fwdat2_wh=np.load(''+arraypath+'b_'+vari+'_'+tname+'.npy')
    fwdat6_wh=np.load(''+arraypath+'w_'+vari+'_'+tname+'.npy')

    datetime2=np.load(''+arraypath+'datetime_'+vari+'_'+tname+'.npy')
    time=np.load(''+arraypath+'time_'+vari+'_'+tname+'.npy')

#        if v=='POHJ':
#    if vari=='wheight':
#        print min(fwdat2_wh)



    print vari



#box plots:

#Defining the sides of the boxes
     

        
    if vari=='wheight':
        wd2=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
        wd6=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
        squares=np.zeros((len(wd2),len(wd6)), dtype=int)

    elif vari=='wdir' or vari=='winddir':
        wd2=[0,30,60,90,120,150,180,210,240,270,300,330,360]
        wd6=[0,30,60,90,120,150,180,210,240,270,300,330,360]
        squares=np.zeros((len(wd2),len(wd6)), dtype=int)

    elif vari=='pperiod':
        wd2=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        wd6=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        squares=np.zeros((len(wd2),len(wd6)), dtype=int)

    elif vari=='period':
        wd2=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        wd6=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        squares=np.zeros((len(wd2),len(wd6)), dtype=int)

    elif vari=='windmag':
        wd2=[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
        wd6=[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
        squares=np.zeros((len(wd2),len(wd6)), dtype=int)



#sijoitetaan havainnot oikeisiin laatikoihin:

    iii=1
    while iii<len(wd2):

        jjj=1
        while jjj<len(wd6):
            ggg=0
            while ggg<len(fwdat2_wh):
                if wd2[iii-1]<=fwdat2_wh[ggg]<wd2[iii] and wd6[jjj-1]<=fwdat6_wh[ggg]<wd6[jjj]:
                    squares[iii-1,jjj-1]=squares[iii-1,jjj-1]+1

                ggg=ggg+1
            jjj=jjj+1
        iii=iii+1

#plot:

    squares = np.ma.array (squares, mask=(squares==0))
    plt.figure(figsize=(12,10))

    if vari=='wdir':
        plt.xlabel(''+tname+' dir [deg]', fontsize=20)
        plt.ylabel('WAM dir [deg]', fontsize=20)
        plt.ylim(0,360)
        plt.xlim(0,360)

            
    elif vari=='winddir':
        plt.xlabel(''+tname+' winddir [deg]', fontsize=20)
        plt.ylabel('WAM winddir [deg]', fontsize=20)
        plt.ylim(0,360)
        plt.xlim(0,360)


    elif vari=='wheight':
        plt.xlabel(''+tname+' $H_s$ [m]',fontsize=20)
#        plt.ylabel('WAM UERRA $H_s$ [m]', fontsize=20)
        plt.ylabel('WAM $H_s$ [m]', fontsize=20)
        plt.ylim(0,10)
        plt.xlim(0,10)



    elif vari=='period':
        plt.xlabel(''+tname+' $T_m$ [s]', fontsize=20)
#        plt.ylabel('WAM UERRA $T_m$ [s]', fontsize=20)
        plt.ylabel('WAM $T_m$ [s]', fontsize=20)
        plt.ylim(0,15)
        plt.xlim(0,15)


    elif vari=='pperiod':
        plt.xlabel(''+tname+' $T_p$ [s]', fontsize=20)
#        plt.ylabel('WAM UERRA $T_p$ [s]', fontsize=20)
        plt.ylabel('WAM $T_p$ [s]', fontsize=20)
        plt.ylim(0,15)
        plt.xlim(0,15)


    elif vari=='windmag':
        plt.xlabel(''+tname+' windmag [m/s]', fontsize=20)
        plt.ylabel('WAM windmag [m/s]', fontsize=20)
        plt.ylim(0,30)
        plt.xlim(0,30)


    Wd2,Wd6=np.meshgrid(wd2,wd6)


    plt.grid(True)



#ylempi norm ilmoittaa colorbarin värit prosenteissa, alempi havaintojen lukumäärissä
    cmap = mpl.colors.ListedColormap(['#cce4ff', '#99c9ff', '#66adff', '#006be6', '#ffff66', '#ffbb33', '#ff9900', '#ff471a', '#e60000'])
    norm = mpl.colors.BoundaryNorm([1/len(fwdat2_wh),0.0001,0.0005,0.001,0.005,0.01,0.05,0.1,0.2,0.3], cmap.N)
#        norm = mpl.colors.BoundaryNorm([0,(len(fwdat2_wh))*0.0001,(len(fwdat2_wh))*0.0005,(len(fwdat2_wh))*0.001,(len(fwdat2_wh))*0.005,(len(fwdat2_wh))*0.01,(len(fwdat2_wh))*0.05,(len(fwdat2_wh))*0.1,(len(fwdat2_wh))*0.2,(len(fwdat2_wh))*0.3], cmap.N)


    squares=squares.astype(float)
    squares=squares/float(len(fwdat2_wh))
    plt.pcolor(Wd6, Wd2, squares, cmap=cmap, norm=norm)
    plt.colorbar(extend='both')
    plt.plot([0,1,2,3,4,5,6,7,8,370], [0,1,2,3,4,5,6,7,8,370], color='k')
#        plt.savefig(''+saveplotpathL+j+'/'+tname+'_'+j+'.png')

#    plt.savefig(''+saveplotpathL+vari+'/'+tname+'_'+vari+'_alt_UERRA.png')
    plt.savefig(''+saveplotpathL+vari+'/'+tname+'_'+vari+'_alt'+plotfix+'.png')



                            
#Tavallinen scatter-kuva:


    plt.figure(figsize=(10,10))
    plt.scatter(fwdat2_wh, fwdat6_wh, alpha=0.5)

    if vari=='wdir':
        plt.ylim(0,360)
        plt.xlim(0,360)
           
    elif vari=='wheight':
        plt.xlabel(''+tname+' Hs [m]', fontsize=20)
        plt.ylabel('WAM Hs [m]', fontsize=20)

    elif vari=='period':
        plt.xlabel(''+tname+' Tz [s]', fontsize=20)
        plt.ylabel('WAM Tz [s]', fontsize=20)

    elif vari=='pperiod':
        plt.xlabel(''+tname+' Tp [s]', fontsize=20)
        plt.ylabel('WAM Tp [s]', fontsize=20)

    plt.grid(True)
    plt.title('scatter_'+vari+'_'+tname+'')

    plt.savefig(''+saveplotpathL+vari+'/'+tname+'_'+vari+'_scatter'+plotfix+'.png')



    plt.clf()




    if vari=='wheight':
        plt.figure(figsize=(10,10))

        q=200
        qx=np.empty(q)
        qy=np.empty(q)


        x=np.sort(fwdat2_wh)
        y=np.sort(fwdat6_wh)
        lx=len(x);
        ly=len(y);
        sx=lx/q;        #step size for x
        sy=ly/q;

    
        for i in range(0,q):
            print math.ceil(i*lx/q)
            qx[i]=x[int(math.ceil(i*lx/q))]
            qy[i]=y[int(math.ceil(i*ly/q))]
        
        plt.scatter(qx,qy, marker='x', s=54)

        plt.xlabel(''+tname+' $H_s$ [m]',fontsize=20)
        plt.ylabel('WAM $H_s$ [m]', fontsize=20)
        plt.ylim(0,10)
        plt.xlim(0,10)

        plt.savefig(''+saveplotpathL+vari+'/'+tname+'_'+vari+'_qq'+plotfix+'.png')                 


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!laatikko+qq!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        plt.figure(figsize=(12,10))

        plt.xlabel(''+tname+' $H_s$ [m]',fontsize=20)
#        plt.ylabel('WAM UERRA $H_s$ [m]', fontsize=20)
        plt.ylabel('WAM $H_s$ [m]', fontsize=20)
        plt.ylim(0,10)
        plt.xlim(0,10)



        Wd2,Wd6=np.meshgrid(wd2,wd6)

        plt.grid(True)
#ylempi norm ilmoittaa colorbarin värit prosenteissa, alempi havaintojen lukumäärissä
        cmap = mpl.colors.ListedColormap(['#cce4ff', '#99c9ff', '#66adff', '#006be6', '#ffff66', '#ffbb33', '#ff9900', '#ff471a', '#e60000'])
        norm = mpl.colors.BoundaryNorm([1/len(fwdat2_wh),0.0001,0.0005,0.001,0.005,0.01,0.05,0.1,0.2,0.3], cmap.N)
#            norm = mpl.colors.BoundaryNorm([0,(len(fwdat2_wh))*0.0001,(len(fwdat2_wh))*0.0005,(len(fwdat2_wh))*0.001,(len(fwdat2_wh))*0.005,(len(fwdat2_wh))*0.01,(len(fwdat2_wh))*0.05,(len(fwdat2_wh))*0.1,(len(fwdat2_wh))*0.2,(len(fwdat2_wh))*0.3], cmap.N)

        squares=squares.astype(float)
        plt.pcolor(Wd6, Wd2, squares, cmap=cmap, norm=norm)
        plt.colorbar(extend='both')
        plt.scatter(qx,qy, marker='x', s=54, color='k')
        plt.plot([0,1,2,3,4,5,6,7,8,370], [0,1,2,3,4,5,6,7,8,370], color='k')

#        plt.savefig(''+saveplotpathL+'/'+vari+'/'+tname+'_'+vari+'_alt_qq_UERRA.png')
        plt.savefig(''+saveplotpathL+'/'+vari+'/'+tname+'_'+vari+'_alt_qq'+plotfix+'.png')

#    datetime2=datetime
    

    datetime2 = np.array(datetime2, dtype='datetime64[s]')

    for idx, j in enumerate(datetime2):
        if idx<7000:
            print(j)

#    plt.figure(figsize=(50,5))
#    print(datetime.datetime(2010,9,20,20,0))

    
    #2010
#    idx1=int(np.where(datetime2== np.datetime64(datetime.datetime(1970, 9, 20, 20, 0)))[0][0])
#    idx2=int(np.where(datetime2== np.datetime64(datetime.datetime(1970, 9, 26, 3, 59, 59)))[0][0])

    #2011
#    idx1=int(np.where(datetime2== np.datetime64(datetime.datetime(1971, 4, 12, 9, 59, 59)))[0][0])
#    idx2=int(np.where(datetime2== np.datetime64(datetime.datetime(1971, 4, 15, 21, 59, 59)))[0][0])

    #2012
#    idx1=int(np.where(datetime2== np.datetime64(datetime.datetime(1972, 9, 19, 18, 59, 59)))[0][0])
#    idx2=int(np.where(datetime2== np.datetime64(datetime.datetime(1972, 11, 5, 12, 59, 59)))[0][0])
#1
#    idx1=int(np.where(datetime2== np.datetime64(datetime.datetime(2012, 9, 27, 6, 59, 59)))[0][0])
#    idx2=int(np.where(datetime2== np.datetime64(datetime.datetime(2012, 11, 5, 12, 59, 59)))[0][0])


    idx1=int(np.where(datetime2== np.datetime64(datetime.datetime(2012, 9, 19, 18, 59, 59)))[0][0])
    idx2=int(np.where(datetime2== np.datetime64(datetime.datetime(2012, 11, 5, 12, 59, 59)))[0][0])

#    idx1=int(np.where(datetime2== np.datetime64(datetime.datetime(1972, 9, 19, 18, 59, 59)))[0][0])
#    idx2=int(np.where(datetime2== np.datetime64(datetime.datetime(1972, 11, 5, 12, 59, 59)))[0][0])

#5
#    idx1=int(np.where(datetime2== np.datetime64(datetime.datetime(2012, 9, 23, 9, 0, 0)))[0][0])
#    idx2=int(np.where(datetime2== np.datetime64(datetime.datetime(2012, 10, 2, 6, 0, 0)))[0][0])
#
#    idx1=int(np.where(datetime2== np.datetime64(datetime.datetime(2012, 9, 24, 0, 0, 0)))[0][0])
#    idx2=int(np.where(datetime2== np.datetime64(datetime.datetime(2012, 9, 27, 11, 0, 0)))[0][0])
#

#    idx1=int(np.where(datetime2== np.datetime64(datetime.datetime(1972, 9, 24, 0, 0, 0)))[0][0])
#    idx2=int(np.where(datetime2== np.datetime64(datetime.datetime(1972, 9, 27, 11, 0, 0)))[0][0])
#
#patk dir
#    idx1=int(np.where(datetime2== np.datetime64(datetime.datetime(1972, 9, 19, 19, 0, 0)))[0][0])
#    idx2=int(np.where(datetime2== np.datetime64(datetime.datetime(1972, 9, 22, 14, 0, 0)))[0][0])


#    idx1=int(np.where(datetime2== np.datetime64(datetime.datetime(1972, 9, 19, 18, 59, 59)))[0][0])
#    idx2=int(np.where(datetime2== np.datetime64(datetime.datetime(1972, 9, 22, 14, 0, 0)))[0][0])

##5
#    idx1=int(np.where(datetime2== np.datetime64(datetime.datetime(1972, 9, 23, 9, 0, 0)))[0][0])
#    idx2=int(np.where(datetime2== np.datetime64(datetime.datetime(1972, 10, 2, 6, 0, 0)))[0][0])


#    print(idx1)
#    print(idx2)
#    print(np.shape(datetime2))

#    print(


#    print(np.shape(datetime2))
#    print(np.shape(fwdat2_wh))

#    fig, ax=plt.subplots(figsize=(50,5))
    fig, ax=plt.subplots(figsize=(15,3))
#    fig, ax=plt.subplots()
#    ps1,=ax.plot(datetime2[(np.where(datetime2== np.datetime64(datetime.datetime(2010,9,20,20,0)))[0][0]):(np.where(datetime2== np.datetime64(datetime.datetime(2010,9,26,4,0)))[0][0])], fwdat2_wh[(np.where(datetime2== np.datetime64(datetime.datetime(2010,9,20,20,0)))[0][0]):(np.where(datetime2== np.datetime64(datetime.datetime(2010,9,26,4,0)))[0][0])], color='k')
#    ps1,=ax.plot(datetime2, fwdat2_wh, color='k')
    ps1,=ax.plot(datetime2[idx1:idx2], fwdat2_wh[idx1:idx2], color='k')
#    ps2,=ax.plot(datetime[np.where(datetime== datetime.datetime(2010,9,20,20,0),datetime)[0]:np.where(datetime== datetime.datetime(2010,9,26,4,0),datetime)[0]], fwdat6_wh[np.where(datetime== datetime.datetime(2010,9,20,20,0),datetime)[0]:np.where(datetime== datetime.datetime(2010,9,26,4,0),datetime)[0]], color='r')
#    ps2,=ax.plot(datetime2, fwdat6_wh, color='r')
    ps2,=ax.plot(datetime2[idx1:idx2], fwdat6_wh[idx1:idx2], color='r')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y %m %d'))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(4))
    fig.legend([ps1,ps2],['buoy','model'], loc=1)
    plt.title(''+vari+'_'+tname+'')
#    plt.savefig(''+saveplotpathL+'/'+vari+'/'+tname+'_'+vari+'_times'+plotfix+'.png')
#    plt.savefig(''+saveplotpathL+'/'+vari+'/'+tname+'_'+vari+'_times_2012_1.png')
#    plt.savefig(''+saveplotpathL+'/'+vari+'/'+tname+'_'+vari+'_times_2012_09_19.png')
    plt.savefig(''+saveplotpathL+'/'+vari+'/'+tname+'_'+vari+'_times_full.png')
#    plt.savefig(''+saveplotpathL+'/'+vari+'/'+tname+'_'+vari+'_times_2012_09_24.png')




    difference=fwdat2_wh[idx1:idx2]-fwdat6_wh[idx1:idx2]
    difference2=np.zeros((len(difference)))
    
    for idx, i in enumerate(difference):
        if i>180:
            print('akgkhdva')
            difference2[idx]=360-i
        elif i<-180:
            difference2[idx]=360+i
        else:
            difference2[idx]=i     


    fig, ax=plt.subplots(figsize=(50,5))

    ps1,=ax.plot(datetime2[idx1:idx2], np.abs(difference2), color='k')

#    ps2,=ax.plot(datetime2[idx1:idx2], fwdat6_wh[idx1:idx2], color='r')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y %m %d'))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.grid(color='r', linestyle='-', linewidth=2, axis='y')
    fig.legend([ps1,ps2],['buoy','model'], loc=1)
    plt.title(''+vari+'_'+tname+'')

#    plt.savefig(''+saveplotpathL+'/'+vari+'/'+tname+'_'+vari+'_times_2012_1diff2.png')
#    plt.savefig(''+saveplotpathL+'/'+vari+'/'+tname+'_'+vari+'_times_2012_5diff2.png')
#    plt.savefig(''+saveplotpathL+'/'+vari+'/'+tname+'_'+vari+'_times_2012_09_19diff2.png')
#    plt.savefig(''+saveplotpathL+'/'+vari+'/'+tname+'_'+vari+'_times_2012_09_24diff2.png')







