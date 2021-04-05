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



arraypath=sys.argv[3]
saveplotpathL=sys.argv[2]


 
for j in [sys.argv[1]]:
    fwdat2_wh=np.empty([0])  
    fwdat6_wh=np.empty([0])  


    for w in sys.argv[4:]:

        tname=''.join(c for c in str(w) if c.isalpha())
        print tname

        dat2=np.load(''+arraypath+'b_'+j+'_'+tname+'.npy')
        dat6=np.load(''+arraypath+'w_'+j+'_'+tname+'.npy')


        fwdat2_wh=np.hstack([fwdat2_wh, dat2])
        fwdat6_wh=np.hstack([fwdat6_wh, dat6])

        print len(fwdat2_wh)

  
#Laatikko-kuvat:

#Tässä määritellään laatikoiden rajat

      
    if j=='wheight':
        wd2=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
        wd6=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
        squares=np.zeros((len(wd2),len(wd6)), dtype=int)

    elif j=='wdir' or j=='winddir':
        wd2=[0,30,60,90,120,150,180,210,240,270,300,330,360]
        wd6=[0,30,60,90,120,150,180,210,240,270,300,330,360]
        squares=np.zeros((len(wd2),len(wd6)), dtype=int)

    elif j=='pperiod':
        wd2=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        wd6=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        squares=np.zeros((len(wd2),len(wd6)), dtype=int)

    elif j=='period':
        wd2=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        wd6=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        squares=np.zeros((len(wd2),len(wd6)), dtype=int)

    elif j=='windmag':
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


#kuva:
    squares = np.ma.array (squares, mask=(squares==0))
    plt.figure(figsize=(12,10))

    if j=='wdir':

        plt.ylabel('WAM dir [deg]', fontsize=20)
        plt.ylim(0,360)
        plt.xlim(0,360)

    elif j=='winddir':
        plt.xlabel('winddir [deg]', fontsize=20)
        plt.ylabel('WAM winddir [deg]', fontsize=20)
        plt.ylim(0,360)
        plt.xlim(0,360)

    elif j=='wheight':
        plt.xlabel(' $H_s$ [m]',fontsize=20)
        plt.ylabel('WAM $H_s$ [m]', fontsize=20)
        plt.ylim(0,10)
        plt.xlim(0,10)

    elif j=='period':
        plt.xlabel(' $T_m$ [s]', fontsize=20)
        plt.ylabel('WAM $T_m$ [s]', fontsize=20)
        plt.ylim(0,15)
        plt.xlim(0,15)

    elif j=='pperiod':
        plt.xlabel(' $T_p$ [s]', fontsize=20)
        plt.ylabel('WAM $T_p$ [s]', fontsize=20)
        plt.ylim(0,15)
        plt.xlim(0,15)

    elif j=='windmag':
        plt.xlabel('windmag [m/s]', fontsize=20)
        plt.ylabel('WAM windmag [m/s]', fontsize=20)
        plt.ylim(0,30)
        plt.xlim(0,30)

    Wd2,Wd6=np.meshgrid(wd2,wd6)


    plt.grid(True)


    cmap = mpl.colors.ListedColormap(['#cce4ff', '#99c9ff', '#66adff', '#006be6', '#ffff66', '#ffbb33', '#ff9900', '#ff471a', '#e60000'])

#ylempi norm ilmoittaa colorbarin värit prosenteissa, alempi havaintojen lukumäärissä
    norm = mpl.colors.BoundaryNorm([1/len(fwdat2_wh),0.0001,0.0005,0.001,0.005,0.01,0.05,0.1,0.2,0.3], cmap.N)
#    norm = mpl.colors.BoundaryNorm([0,(len(fwdat2_wh))*0.0001,(len(fwdat2_wh))*0.0005,(len(fwdat2_wh))*0.001,(len(fwdat2_wh))*0.005,(len(fwdat2_wh))*0.01,(len(fwdat2_wh))*0.05,(len(fwdat2_wh))*0.1,(len(fwdat2_wh))*0.2,(len(fwdat2_wh))*0.3], cmap.N)


    squares=squares.astype(float)
    squares=squares/float(len(fwdat2_wh))
    
    plt.pcolor(Wd6, Wd2, squares, cmap=cmap, norm=norm)
    plt.colorbar(extend='both')
    plt.plot([0,1,2,3,4,5,6,7,8,370], [0,1,2,3,4,5,6,7,8,370], color='k')
    plt.savefig(''+saveplotpathL+j+'/'+j+'.png')
                            

#Tavallinen scatter-kuva:

    plt.figure(figsize=(10,10))

    plt.scatter(fwdat2_wh, fwdat6_wh, alpha=0.5)
    if j=='wdir':
        plt.ylim(0,360)
        plt.xlim(0,360)

    elif j=='winddir':
        plt.xlabel('winddir [deg]', fontsize=20)
        plt.ylabel('WAM winddir [deg]', fontsize=20)
            
    elif j=='wheight':
        plt.xlabel('Hs [m]', fontsize=20)
        plt.ylabel('WAM Hs [m]', fontsize=20)

    elif j=='period':
        plt.xlabel('Tz [s]', fontsize=20)
        plt.ylabel('WAM Tz [s]', fontsize=20)


    elif j=='pperiod':
        plt.xlabel('Tp [s]', fontsize=20)
        plt.ylabel('WAM Tp [s]', fontsize=20)


    elif j=='windmag':
        plt.xlabel('windmag [m/s]', fontsize=20)
        plt.ylabel('WAM windmag [m/s]', fontsize=20)


    plt.grid(True)
    plt.title('scatter_'+j+'')

    plt.savefig(''+saveplotpathL+j+'/'+j+'_scatter.png')

    plt.clf()



#qq

    if j=='wheight':
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
#        m=max(max(x),max(y));
    
        for i in range(0,q):
            qx[i]=x[int(math.ceil(i*lx/q))]
            qy[i]=y[int(math.ceil(i*ly/q))]
        
        plt.scatter(qx,qy, marker='x', s=54)
       

        plt.xlabel('$H_s$ [m]',fontsize=20)
        plt.ylabel('WAM $H_s$ [m]', fontsize=20)
        plt.ylim(0,10)
        plt.xlim(0,10)

        plt.savefig(''+saveplotpathL+j+'/'+j+'_qq.png')                 


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!laatikko+qq!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        plt.figure(figsize=(12,10))

        plt.xlabel('$H_s$ [m]',fontsize=20)
        plt.ylabel('WAM $H_s$ [m]', fontsize=20)
        plt.ylim(0,10)
        plt.xlim(0,10)


        Wd2,Wd6=np.meshgrid(wd2,wd6)

        plt.grid(True)

#ylempi norm ilmoittaa colorbarin värit prosenteissa, alempi havaintojen lukumäärissä
        cmap = mpl.colors.ListedColormap(['#cce4ff', '#99c9ff', '#66adff', '#006be6', '#ffff66', '#ffbb33', '#ff9900', '#ff471a', '#e60000'])
        norm = mpl.colors.BoundaryNorm([1/len(fwdat2_wh),0.0001,0.0005,0.001,0.005,0.01,0.05,0.1,0.2,0.3], cmap.N)
#        norm = mpl.colors.BoundaryNorm([0,(len(fwdat2_wh))*0.0001,(len(fwdat2_wh))*0.0005,(len(fwdat2_wh))*0.001,(len(fwdat2_wh))*0.005,(len(fwdat2_wh))*0.01,(len(fwdat2_wh))*0.05,(len(fwdat2_wh))*0.1,(len(fwdat2_wh))*0.2,(len(fwdat2_wh))*0.3], cmap.N)

        squares=squares.astype(float)

        plt.pcolor(Wd6, Wd2, squares, cmap=cmap, norm=norm)

        plt.colorbar(extend='both')

        plt.scatter(qx,qy, marker='x', s=54, color='k')
        plt.plot([0,1,2,3,4,5,6,7,8,370], [0,1,2,3,4,5,6,7,8,370], color='k')

        plt.savefig(''+saveplotpathL+'/'+j+'/'+j+'_alt_qq.png')


