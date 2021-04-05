#! /usr/bin/env python
#-*- coding: utf-8 -*-
#2/2019, Olga Vähä-Piikkiö



import numpy as np
import matplotlib
matplotlib.use('Agg') # ensure that X11 is not used, this script is intended for server use
import matplotlib.pyplot as plt
import subprocess
#from scipy.stats import nanmean
from scipy.io import netcdf
import scipy
import os
import math
import matplotlib as mpl
import sys


orig=sys.argv[2]
prefix=sys.argv[3]
arraypath2=sys.argv[5]
buoypath=sys.argv[6]
arraypath=sys.argv[7]


vari=sys.argv[4] 

for v in [sys.argv[1]]:
    
    tname=v
#    tname=w[:-3]
#    tname=tname[9:]

    print tname
    

#    tname=w[:-3]
#    tname=tname[9:]


    print tname
 

    wdat210=np.load(''+arraypath+'2'+vari+'_b_'+tname+'.npy')
    wdat610=np.load(''+arraypath+'2'+vari+'_w_'+tname+'.npy')

    idxarray=np.load(''+arraypath+'2idxarray_b_'+tname+'.npy')
    time=np.load(''+arraypath+'2time_w_'+tname+'.npy')
    datetime=np.load(''+arraypath+'2datetime_w_'+tname+'.npy')

    print datetime
    print time


    print np.shape(wdat610)
    print np.shape(wdat210)





#Removing others than quality class 1:

#        for yrmon in yearmonth:
    qc=np.empty([0])  

    if orig=='cmems':
        for yrmon in sys.argv[8:]:

            yrmon=''.join(c for c in str(yrmon) if c.isdigit())
 
            try:
                c_HELS=subprocess.Popen(['ls -d '+buoypath+'/'+v+'/BO_'+yrmon+'_TS_MO_'+v+'.nc'], shell=True, stdout=subprocess.PIPE)
            except IOError:
                continue
            newest_HELS=c_HELS.communicate()[0].strip()
            try:
                newesta=netcdf.netcdf_file(newest_HELS, 'r')
            except (TypeError, IOError, AttributeError, ValueError) as e:
                continue


            if vari=='wheight':
                try:
                    qcb=newesta.variables['VHM0_QC'][:,0]    
                except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                    try:
                        qcb=newesta.variables['VTDH_qc'][:,0]
                    except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                        try:
                            qcb=newesta.variables['VHM0_QC'][:]  
                        except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:   
                            qcb=newesta.variables['VTDH_QC'][:]



            elif vari=='pperiod':
                try:
                    qcb=newesta.variables['VTPK_QC'][:,0]    
                except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                    try:
                        qcb=newesta.variables['VTPK_QC'][:]  
                    except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                        qcb=np.zeros((len(datetime))) #nämä 0-arrayt ovat vain muodon vuoksi tässä 



            elif vari=='period':
                try:
                    qcb=newesta.variables['VTZA_QC'][:,0]
                except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                    try:
                        qcb=newesta.variables['VTZA_QC'][:]
                    except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                        qcb=np.zeros((len(datetime)))



            elif vari=='wdir':
                try:
                    qcb=newesta.variables['VMDR_QC'][:,0]        
                except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                    try:
                        qcb=newesta.variables['VPED_QC'][:,0]        
                    except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:  
                        try:
                            qcb=newesta.variables['VMDR_QC'][:]
                        except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e: 
                            try:
                                qcb=newesta.variables['VPED_QC'][:]        
                            except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:                         
                                qcb=np.zeros((len(datetime)))




            qc=np.hstack([qc, qcb])

#        for i in idxarray:
#            i=i-1 
            
#        print idxarray

#        idxarray=idxarray-1
        print idxarray

        print np.shape(qc)
        print np.shape(idxarray)
        qc = [qc[i] for i in idxarray]
        qc=np.asarray(qc)

        wdat2qc=np.ma.masked_where(qc!=1, wdat210)
        qc2=np.ma.masked_where(qc!=1, qc)
        wdat6qc=np.ma.masked_where(qc!=1, wdat610)


        time=np.reshape(time, (len(time[:])))
#        time=np.reshape(time, (len(time[:,0])))
        time=np.ma.masked_where(qc!=1, time)
        datetime=np.ma.masked_where(qc!=1, datetime)



        if v=='VaderoarnaWR':
            if vari=='pperiod':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>25))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>25))
                datetime=np.ma.array(datetime, mask=(wdat2qc>25))
                time=np.ma.array(time, mask=(wdat2qc>25))


        if v=='DarsserSWR':
            if vari=='pperiod':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>9.9))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>9.9))
                datetime=np.ma.array(datetime, mask=(wdat2qc>9.9))
                time=np.ma.array(time, mask=(wdat2qc>9.9))
 

        if v=='HuvudskarOst':
            if vari=='pperiod':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>22))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>22))
                datetime=np.ma.array(datetime, mask=(wdat2qc>22))
                time=np.ma.array(time, mask=(wdat2qc>22))


        if v=='Knollsgrund':
            if vari=='period':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>10))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>10))
                datetime=np.ma.array(datetime, mask=(wdat2qc>10))
                time=np.ma.array(time, mask=(wdat2qc>10))

        if v=='NorthernBaltic':
            if vari=='wheight':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>8.3))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>8.3))                 
                time=np.ma.array(time, mask=(wdat2qc>8.3)) 
                datetime=np.ma.array(datetime, mask=(wdat2qc>8.3))

            if vari=='wheight':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat6qc<0))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat6qc<0))                 
                time=np.ma.array(time, mask=(wdat6qc<0)) 
                datetime=np.ma.array(datetime, mask=(wdat6qc<0))

            if vari=='pperiod':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc<0))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc<0))                 
                time=np.ma.array(time, mask=(wdat2qc<0)) 
                datetime=np.ma.array(datetime, mask=(wdat2qc<0))

            if vari=='pperiod':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat6qc<0))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat6qc<0))                 
                time=np.ma.array(time, mask=(wdat6qc<0)) 
                datetime=np.ma.array(datetime, mask=(wdat6qc<0))



        if v=='ArkonaWR':
            if vari=='wheight':
                wdat2qc=np.ma.array(wdat2qc, mask=((wdat2qc>5) & (wdat6qc<2.5)))
                wdat6qc=np.ma.array(wdat6qc, mask=((wdat2qc>5) & (wdat6qc<2.5)))                 
                time=np.ma.array(time, mask=((wdat2qc>5) & (wdat6qc<2.5))) 
                datetime=np.ma.array(datetime, mask=((wdat2qc>5) & (wdat6qc<2.5)))


        if v=='BothnianSea':
            if vari=='wheight':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc==0))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc==0))                 
                time=np.ma.array(time, mask=(wdat2qc==0)) 
                datetime=np.ma.array(datetime, mask=(wdat2qc==0))


        if v=='FinngrundetWR':
            if vari=='wheight':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>15))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>15))                 
                time=np.ma.array(time, mask=(wdat2qc>15)) 
                datetime=np.ma.array(datetime, mask=(wdat2qc>15))

            elif vari=='pperiod':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>20))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>20))                 
                time=np.ma.array(time, mask=(wdat2qc>20)) 
                datetime=np.ma.array(datetime, mask=(wdat2qc>20))

            elif vari=='period':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>16))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>16))                 
                time=np.ma.array(time, mask=(wdat2qc>16)) 
                datetime=np.ma.array(datetime, mask=(wdat2qc>16))





######################################################################################################



    else:

        wdat2qc=np.ma.array(wdat210, mask=(wdat210<0))
        wdat6qc=np.ma.array(wdat610, mask=(wdat210<0))                
        time=np.ma.array(time, mask=(wdat210<0)) 
        datetime=np.ma.array(datetime, mask=(wdat210<0)) 
        


        if v=='BothnianSea':
            if vari=='wheight':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>7))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>7))                 
                time=np.ma.array(time, mask=(wdat2qc>7)) 
                datetime=np.ma.array(datetime, mask=(wdat2qc>7))
                
            if vari=='pperiod':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>20))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>20))  
                time=np.ma.array(time, mask=(wdat2qc>20)) 
                datetime=np.ma.array(datetime, mask=(wdat2qc>20))        

        if v=='HelsinkiBuoy':
            if vari=='pperiod':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>12))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>12)) 
                time=np.ma.array(time, mask=(wdat2qc>12)) 
                datetime=np.ma.array(datetime, mask=(wdat2qc>12))     
        if v=='NorthernBaltic':
            if vari=='pperiod':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>14))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>14)) 
                time=np.ma.array(time, mask=(wdat2qc>14)) 
                datetime=np.ma.array(datetime, mask=(wdat2qc>14))  


            if vari=='wheight':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>8.3))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>8.3))                 
                time=np.ma.array(time, mask=(wdat2qc>8.3)) 
                datetime=np.ma.array(datetime, mask=(wdat2qc>8.3))

        if v=='BothnianBay':
            if vari=='pperiod':
                wdat2qc=np.ma.array(wdat2qc, mask=(wdat2qc>12))
                wdat6qc=np.ma.array(wdat6qc, mask=(wdat2qc>12)) 
                time=np.ma.array(time, mask=(wdat2qc>12)) 
                datetime=np.ma.array(datetime, mask=(wdat2qc>12))     

            if vari=='wheight':

                wdat2qc=np.ma.array(wdat2qc, mask=((wdat2qc>2.7) & (wdat6qc<0.8)))
                wdat6qc=np.ma.array(wdat6qc, mask=((wdat2qc>2.7) & (wdat6qc<0.8)))                 
                time=np.ma.array(time, mask=((wdat2qc>2.7) & (wdat6qc<0.8))) 
                datetime=np.ma.array(datetime, mask=((wdat2qc>2.7) & (wdat6qc<0.8)))

#######################################################################tyomaa alkaa
#    date_format = "%d/%m/%Y"

#    manufacturing_date = datetime.strptime(datetime,date_format)

#if (datetime.strptime("1/1/2001", date_format) <= manufacturing_date < datetime.strptime("31/1/2008", date_format)):
    #do something

#    wdat2qc=np.ma.array(wdat2qc, mask=(datetime))
#    wdat6qc=np.ma.array(wdat6qc, mask=((wdat2qc>2.7) & (wdat6qc<0.8)))                 
#    time=np.ma.array(time, mask=((wdat2qc>2.7) & (wdat6qc<0.8))) 
#    datetime=np.ma.array(datetime, mask=((wdat2qc>2.7) & (wdat6qc<0.8)))

#######################################################################tyomaa loppuu

    np.ma.set_fill_value(wdat2qc, -999)
    np.ma.set_fill_value(wdat6qc, -999)
    np.ma.set_fill_value(time, -999)
    np.ma.set_fill_value(datetime, -999)

    wdat2=wdat2qc.filled()
    wdat6=wdat6qc.filled()
    time=time.filled()
    datetime=datetime.filled()



    fwdat2_wh=wdat2
    fwdat6_wh=wdat6




    wherehs=np.where(fwdat2_wh==-999)

    pppp=0
      
    while pppp<len(wherehs):
        fwdat2_wh=np.delete(fwdat2_wh, wherehs[pppp]-pppp)
        fwdat6_wh=np.delete(fwdat6_wh, wherehs[pppp]-pppp)

        time=np.delete(time, wherehs[pppp]-pppp)
        datetime=np.delete(datetime, wherehs[pppp]-pppp)


        pppp=pppp+1


    print vari



#Saving into text files and numpy arrays.


    np.savetxt(''+arraypath2+'/b_'+vari+'_'+tname+'', fwdat2_wh, delimiter=' ', newline='\n', header='', footer='')
    np.savetxt(''+arraypath2+'/w_'+vari+'_'+tname+'', fwdat6_wh, delimiter=' ', newline='\n', header='', footer='')
    np.savetxt(''+arraypath2+'/time_'+vari+'_'+tname+'', datetime, delimiter=' ', newline='\n', header='', footer='', fmt="%s")
    np.savetxt(''+arraypath2+'/time2_'+vari+'_'+tname+'', time, delimiter=' ', newline='\n', header='', footer='', fmt="%s")

    np.save(''+arraypath+'b_'+vari+'_'+tname+'', fwdat2_wh)
    np.save(''+arraypath+'w_'+vari+'_'+tname+'', fwdat6_wh)
    np.save(''+arraypath+'time_'+vari+'_'+tname+'', time)
    np.save(''+arraypath+'datetime_'+vari+'_'+tname+'', datetime)

 

    print np.shape(fwdat2_wh)

        


#Calculating and printing statistics

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
    print tname
    print vari
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








