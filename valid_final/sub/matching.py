#! /usr/bin/env python
#-*- coding: utf-8 -*-
#2/2019, Olga Vähä-Piikkiö


import numpy as np
from scipy.io import netcdf
import matplotlib
matplotlib.use('Agg') # ensure that X11 is not used, this script is intended for server use
import matplotlib.pyplot as plt
import subprocess
import time
import datetime
import os
from scipy.io import netcdf
from scipy import interpolate
import gzip
import fileinput
import sys
import operator

prefix=sys.argv[2]
wampath=sys.argv[4]
buoypath=sys.argv[5]
savearraypath=sys.argv[6]



def find_nearest(array, value):
    idx=(np.abs(array-value)).argmin()
    return idx


def create_modelvarfull(wampath,prefix,yrmon,tname,case):
#    if case=='1point':
#        c_HELS=subprocess.Popen(['ls -d '+wampath+'/'+prefix+str(yrmon)+'_'+tname+'.nc'], shell=True, stdout=subprocess.PIPE)
#        newest_HELS=c_HELS.communicate()[0].strip()
#        try:
#            newesta=netcdf.netcdf_file(newest_HELS, 'r')
#        except (IOError) as e:
#            continue
#            try:
#    elif case=='pick1point' or 'moving':

    global modelvarfull
    yrmon=''.join(c for c in str(yrmon) if c.isdigit())

    c_HELS=subprocess.Popen(['ls -d '+wampath+'/'+prefix+str(yrmon)+'.nc'], shell=True, stdout=subprocess.PIPE)
    newest_HELS=c_HELS.communicate()[0].strip()
#        try:
    newesta=netcdf.netcdf_file(newest_HELS, 'r')
#        except (IOError) as e:
#            continue

    longitudesss=newesta.variables['longitude'][:]
    latitudesss=newesta.variables['latitude'][:]


    maxlonn=find_nearest(longitudesss, maxblon)
    maxlatt=find_nearest(latitudesss, maxblat)
            
    minlonn=find_nearest(longitudesss, minblon)
    minlatt=find_nearest(latitudesss, minblat)


    longitudes=newesta.variables['longitude'][minlonn:maxlonn]
    latitudes=newesta.variables['latitude'][minlatt:maxlatt]

    modelvarfull=np.empty([0,len(latitudes),len(longitudes)])  


    return modelvarfull




vari=sys.argv[3]
case=sys.argv[7]
#print vari
for v in [sys.argv[1]]:
    

    tname=v
#    tname=w[:-3]
#    tname=tname[9:]
#    print tname

    bettime=np.empty([0])
    dates=np.empty([0])
    buoydatess=np.empty([0])

    year_HELS=np.empty([0])
    yr_HELS=np.empty([0])
    mon_HELS=np.empty([0])
    day_HELS=np.empty([0])
    time_HELS=np.empty([0])
    idxarray=np.empty([0], dtype=int)

    buoyvarfull=np.empty([0])  
    datettime=np.empty([0])  

    if not case=='moving':
#        modelvarfull=np.empty([0,400,856])  
#        modelvarfull=np.empty([0,200:400,300:600])  
#    else:
        modelvarfull=np.empty([0])  
    datettimeww3=np.empty([0])  










#######################################################################################################################################
#buoys#
#######################################################################################################################################
    for yrmon in sys.argv[10:]:

        yrmon=''.join(c for c in str(yrmon) if c.isdigit())

        print yrmon

        try:
            c_HELS=subprocess.Popen(['ls -d '+buoypath+'/'+v+'/BO_'+str(yrmon)+'_TS_MO_'+v+'.nc'], shell=True, stdout=subprocess.PIPE)
        except IOError:
            continue

        newest_HELS=c_HELS.communicate()[0].strip()

        try:
            newesta=netcdf.netcdf_file(newest_HELS, 'r')
        except (TypeError, IOError, AttributeError, ValueError) as e:
            continue



        datettimeb=newesta.variables['TIME'][:]

        if vari=='wheight':
            try:
                buoyvar=newesta.variables['VHM0'][:,0]    
            except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                try:
                    buoyvar=newesta.variables['VTDH'][:,0]
                except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                    try:
                        buoyvar=newesta.variables['VHM0'][:]  
                    except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:   
                        buoyvar=newesta.variables['VTDH'][:]



        elif vari=='pperiod':
            try:
                buoyvar=newesta.variables['VTPK'][:,0]    
            except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                try:
                    buoyvar=newesta.variables['VTPK'][:]  
                except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                    buoyvar=np.zeros((len(datettimeb))) #nämä 0-arrayt ovat vain muodon vuoksi tässä 



        elif vari=='period':
            try:
                buoyvar=newesta.variables['VTZA'][:,0]
            except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                try:
                    buoyvar=newesta.variables['VTZA'][:]
                except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                    buoyvar=np.zeros((len(datettimeb)))
#            print buoyvar 


        elif vari=='wdir':
            try:
                buoyvar=newesta.variables['VMDR'][:,0]        
            except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:
                try:
                    buoyvar=newesta.variables['VPED'][:,0]        
                except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:  
                    try:
                        buoyvar=newesta.variables['VMDR'][:]
                    except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e: 
                        try:
                            buoyvar=newesta.variables['VPED'][:]        
                            print('suunta')
                        except (TypeError, IOError, AttributeError, ValueError, IndexError, KeyError) as e:         
                            print('eitanne')                
                            buoyvar=np.zeros((len(datettimeb)))

        elif vari=='winddir':
            buoyvar=newesta.variables['windd'][:]

        elif vari=='windmag':
            buoyvar=newesta.variables['windm'][:]



        if case=='moving':
            blongitude=newesta.variables['longitude'][:]
            blatitude=newesta.variables['latitude'][:]

            minblon=min(blongitude)
            minblat=min(blatitude)

            maxblon=max(blongitude)
            maxblat=max(blatitude)


        datettime=np.hstack([datettime, datettimeb])
        buoyvarfull=np.hstack([buoyvarfull, buoyvar])
        print(buoyvarfull)


#    tim=datetime.datetime(1990,1,1)
    tim=datetime.datetime(1950,1,1)
    for idx, i in enumerate(datettime):

        timestamp=str(tim+datetime.timedelta(days=(float(datettime[idx]))))


        bettime=np.hstack([bettime, timestamp])


             
        year_HELS=np.hstack([year_HELS, timestamp[0:4]])
        yr_HELS=np.hstack([yr_HELS, timestamp[2:4]])        
        mon_HELS=np.hstack([mon_HELS, timestamp[5:7]])

        day_HELS=np.hstack([day_HELS, timestamp[8:10]])
        time_HELS=np.hstack([time_HELS, ''+timestamp[11:13]+'.'+timestamp[14:16]+''])



        buoydate=tim+datetime.timedelta(days=(float(datettime[idx])))


        buoydatess=np.hstack([buoydatess, buoydate])
    

###########################################################################################################

    if case=='moving':
#        modelvarfull=np.empty([0,len(modelvar[0,:,0]),len(modelvar[0,0,:])])  
#        modelvarfull=np.empty([0,0,0])  
#        modelvarfull=1
        create_modelvarfull(wampath,prefix,sys.argv[10],tname,case)
        print np.shape(modelvarfull)


    for yrmon in sys.argv[10:]:

        yrmon=''.join(c for c in str(yrmon) if c.isdigit())
#        print yrmon

#######################################################################################################################################
#ww3#
#######################################################################################################################################
#        c_HELS=subprocess.Popen(['ls -d '+wampath+'/'+prefix+str(yrmon)+'.nc'], shell=True, stdout=subprocess.PIPE)
#        newest_HELS=c_HELS.communicate()[0].strip()
#        newesta=netcdf.netcdf_file(newest_HELS, 'r')

        

        if case=='1point':
            c_HELS=subprocess.Popen(['ls -d '+wampath+'/'+prefix+str(yrmon)+'_'+tname+'.nc'], shell=True, stdout=subprocess.PIPE)
            newest_HELS=c_HELS.communicate()[0].strip()
            try:
                newesta=netcdf.netcdf_file(newest_HELS, 'r')
            except (IOError) as e:
                continue
#            try:
        elif case=='pick1point' or 'moving':
            c_HELS=subprocess.Popen(['ls -d '+wampath+'/'+prefix+str(yrmon)+'.nc'], shell=True, stdout=subprocess.PIPE)
            newest_HELS=c_HELS.communicate()[0].strip()
            try:
                newesta=netcdf.netcdf_file(newest_HELS, 'r')
            except (IOError) as e:
                continue

#            print c_HELS


#        print c_HELS

#        newest_HELS=c_HELS.communicate()[0].strip()

#        try:
#            newesta=netcdf.netcdf_file(newest_HELS, 'r')
#        except (TypeError, IOError, AttributeError, ValueError) as e:
#            continue


#################################################################pick1point


        if case=='pick1point': 

            longitudes=newesta.variables['longitude'][:]
            latitudes=newesta.variables['latitude'][:]

            blon=sys.argv[8]
            blat=sys.argv[9]



            lonn=find_nearest(longitudes, float(blon))
            latt=find_nearest(latitudes, float(blat))


   #####################tahan tarvitaan vaihtoehdot wamille try except +missa fp?

            datettimew=newesta.variables['time'][:]
            if vari=='wheight':
                modelvar=newesta.variables['hs'][:,latt,lonn]
            elif vari=='pperiod':
                modelvar=newesta.variables['fp'][:,latt,lonn]
                modelvar=1/modelvar
#                print modelvar
            elif vari=='period':
                modelvar=newesta.variables['t02'][:,latt,lonn]
            elif vari=='wdir':
#                modelvar=np.zeros((len(datettimew))) 
#############stokesdir
#                udir=newesta.variables['uuss'][:,latt,lonn] 
#                vdir=newesta.variables['vuss'][:,latt,lonn] 

#                modelvar=np.degrees(np.arctan2(udir,vdir))
#                modelvar=modelvar+180
#######################
                modelvar=newesta.variables['dir'][:,latt,lonn]
                print(modelvar)
            elif vari=='winddir':
                uwind=newesta.variables['uwnd'][:,latt,lonn]
                vwind=newesta.variables['vwnd'][:,latt,lonn]

#                wnddw=np.zeros([len(uwind)])
#                for i in range(len(uwind)):
#                    if uwind[i]>=0 and vwind[i]>=0:
#                        wnddw[i]=np.degrees(np.arctan(abs(vwind[i])/abs(uwind[i])))
#                    if uwind[i]>=0 and vwind[i]<0:
#                        wnddw[i]=np.degrees(np.arctan(abs(vwind[i])/abs(uwind[i])))+90
#                    if uwind[i]<0 and vwind[i]<0:
#                        wnddw[i]=np.degrees(np.arctan(abs(vwind[i])/abs(uwind[i])))+180
#                    if uwind[i]<0 and vwind[i]>=0:
#                        wnddw[i]=np.degrees(np.arctan(abs(vwind[i])/abs(uwind[i])))+270

#                modelvar=np.degrees(np.arctan2(vwind,uwind))
#                modelvar=np.empty([1])
 
                modelvar=np.degrees(np.arctan2(uwind,vwind))
                modelvar=modelvar+180
#                wnddw=wnddw+180


#                for r in wnddw:
#                    r=r+float(360)
#                    if r>=360:
#                        r=r-float(360)
#                    print r
##                    else:
##                        r=r

#                    modelvar=np.vstack([modelvar, r])
#                modelvar=np.reshape(modelvar[1:], len(uwind))


#                modelvar=wnddw

            elif vari=='windmag':
                uwind=newesta.variables['uwnd'][:,latt,lonn]
                vwind=newesta.variables['vwnd'][:,latt,lonn]

                wndmw=np.zeros([len(uwind)])
                for i in range(len(uwind)):
                    wndmw[i]=np.sqrt((abs(uwind[i])**2)+(abs(vwind[i])**2))
                modelvar=wndmw





#################################################################moving


        if case=='moving': 

#            modelvar=np.zeros([len(blon)])  

            longitudesss=newesta.variables['longitude'][:]
            latitudesss=newesta.variables['latitude'][:]


            maxlonn=find_nearest(longitudesss, maxblon)
            maxlatt=find_nearest(latitudesss, maxblat)
            
            minlonn=find_nearest(longitudesss, minblon)
            minlatt=find_nearest(latitudesss, minblat)


            longitudes=newesta.variables['longitude'][minlonn:maxlonn]
            latitudes=newesta.variables['latitude'][minlatt:maxlatt]
            datettimew=newesta.variables['time'][:]

            print np.shape(datettimew)
#            for i, (blon, blat) in enumerate(zip(blongitude, blatitude)):
#                lonn=find_nearest(longitudes, blon)
#                latt=find_nearest(latitudes, blat)


   #####################tahan tarvitaan vaihtoehdot wamille try except +missa fp?


            if vari=='wheight':
                modelvar=newesta.variables['hs'][:,minlatt:maxlatt,minlonn:maxlonn]
            elif vari=='pperiod':
                modelvar=newesta.variables['fp'][:,minlatt:maxlatt,minlonn:maxlonn]
#            print modelvar
            elif vari=='period':
                modelvar=newesta.variables['t02'][:,minlatt:maxlatt,minlonn:maxlonn]
            elif vari=='wdir':
                modelvar=np.zeros((len(datettimew))) 
            elif vari=='winddir':
                uwind=newesta.variables['uwnd'][:,minlatt:maxlatt,minlonn:maxlonn]
                vwind=newesta.variables['vwnd'][:,minlatt:maxlatt,minlonn:maxlonn]

#                wnddw=np.zeros([len(uwind)])

#                for i in range(len(uwind)):
#                    if uwind[i]>=0 and vwind[i]>=0:
#                        wnddw[i]=np.arctan(abs(vwind[i])/abs(uwind[i]))
#                    if uwind[i]>=0 and vwind[i]<0:
#                        wnddw[i]=np.arctan(abs(vwind[i])/abs(uwind[i]))+90
#                    if uwind[i]<0 and vwind[i]<0:
#                        wnddw[i]=np.arctan(abs(vwind[i])/abs(uwind[i]))+180
#                    if uwind[i]<0 and vwind[i]>=0:
#                        wnddw[i]=np.arctan(abs(vwind[i])/abs(uwind[i]))+270
                modelvar=np.degrees(np.arctan2(uwind,vwind))
                modelvar=modelvar+180



#                for r in modelvar:
#                    r=r+float(180)
#                    if r>=360:
#                        r=r-float(360)
##                    else:
##                modelvar=wnddw

            elif vari=='windmag':
                wndmw=np.zeros([len(uwind)])
                for i in range(len(uwind)):
                    wndmw[i]=np.sqrt((abs(uwind[i])**2)+(abs(vwind[i])**2))
                modelvar=wndmw





####################################################################################1point



        elif case=='1point':
   #####################tahan tarvitaan vaihtoehdot wamille try except +missa fp?

            datettimew=newesta.variables['time'][:]
            if vari=='wheight':
                modelvar=newesta.variables['hs'][:]
            elif vari=='pperiod':
                modelvar=newesta.variables['fp'][:]
#                print modelvar
            elif vari=='period':
                modelvar=newesta.variables['t02'][:]
            elif vari=='wdir':
                modelvar=np.zeros((len(datettimew))) 
            elif vari=='winddir':
                uwind=newesta.variables['uwnd'][:]
                vwind=newesta.variables['vwnd'][:]

#                wnddw=np.zeros([len(uwind)])
#                for i in range(len(uwind)):
#                    if uwind[i]>=0 and vwind[i]>=0:
#                        wnddw[i]=np.arctan(abs(vwind[i])/abs(uwind[i]))
#                    if uwind[i]>=0 and vwind[i]<0:
#                        wnddw[i]=np.arctan(abs(vwind[i])/abs(uwind[i]))+90
#                    if uwind[i]<0 and vwind[i]<0:
#                        wnddw[i]=np.arctan(abs(vwind[i])/abs(uwind[i]))+180
#                    if uwind[i]<0 and vwind[i]>=0:
#                        wnddw[i]=np.arctan(abs(vwind[i])/abs(uwind[i]))+270
#                modelvar=wnddw

                modelvar=np.degrees(np.arctan2(uwind,vwind))
                modelvar=modelvar+180



#                for r in modelvar:
#                    noop=r+float(180)
#                    if noop>=360:
#                        noopr=noop-float(360)
##                    else:
##                        r=r



#                    modelvar=np.vstack([wdir3, noop])
#                wdirum=np.reshape(wdir3, len(uwind))


            elif vari=='windmag':
                wndmw=np.zeros([len(uwind)])
                for i in range(len(uwind)):
                    wndmw[i]=np.sqrt((abs(uwind[i])**2)+(abs(vwind[i])**2))
                modelvar=wndmw




##########################################################################################

        datettimeww3=np.hstack([datettimeww3, datettimew])
        print np.shape(datettimeww3)
#        if case=='moving':
#            modelvarfull=np.empty([0,len(modelvar[0,:,0]),len(modelvar[0,0,:])])  

        print np.shape(modelvar)
        print np.shape(modelvar)
        if case=='moving':      
            modelvarfull=np.vstack([modelvarfull, modelvar])
        else:
            modelvarfull=np.hstack([modelvarfull, modelvar])

#you might have to modify these
#    tim=datetime.datetime(1990,1,1)
    tim=datetime.datetime(1950,1,1)
    for idx, i in enumerate(datettimeww3):

        timestamp=tim+datetime.timedelta(days=(float(datettimeww3[idx])))


        dates=np.hstack([dates, timestamp])


        print np.shape(dates)

########################################################################################################



    matchmodelvar=np.empty([0])  
    datettimeww3w=np.empty([0])  
    datesww3w=np.empty([0])  

    matchbuoyvar=np.empty([0])  
    datettimeww3b=np.empty([0]) 

    print buoyvarfull
#    if case=='moving':

    for idx,(buoyydate,buoyv) in enumerate(zip(buoydatess,buoyvarfull)):

        closest_idx=find_nearest(dates,buoyydate)

        days, seconds = abs(buoyydate-dates[closest_idx]).days, abs(buoyydate-dates[closest_idx]).seconds
        time_mins_t=days * 24 *60 + seconds / float(60) 

        
        if time_mins_t<20:

#            for i, (blon, blat) in enumerate(zip(blongitude, blatitude)):

            if case=='moving':
                lonn=find_nearest(longitudes, blongitude[idx])
                latt=find_nearest(latitudes, blatitude[idx])
                
                matchmodelvar=np.hstack([matchmodelvar, modelvarfull[closest_idx,latt,lonn]]) 

            else:
                matchmodelvar=np.hstack([matchmodelvar, modelvarfull[closest_idx]]) 

            datettimeww3w=np.hstack([datettimeww3w, datettimeww3[closest_idx]]) 
            datesww3w=np.hstack([datesww3w, dates[closest_idx]]) 

            matchbuoyvar=np.hstack([matchbuoyvar, buoyv]) 
            datettimeww3b=np.hstack([datettimeww3b, buoyydate]) 

            idxarray=np.hstack([idxarray, closest_idx])

        else:
            pass


#    else:
#        for buoyydate,buoyv in zip(buoydatess,buoyvarfull):

#            closest_idx=find_nearest(dates,buoyydate)

#            days, seconds = abs(buoyydate-dates[closest_idx]).days, abs(buoyydate-dates[closest_idx]).seconds
#            time_mins_t=days * 24 *60 + seconds / float(60) 

        
#            if time_mins_t<20:
#                print time_mins_t

#                matchmodelvar=np.hstack([matchmodelvar, modelvarfull[closest_idx]]) 
#                datettimeww3w=np.hstack([datettimeww3w, datettimeww3[closest_idx]]) 
#                datesww3w=np.hstack([datesww3w, dates[closest_idx]]) 

#                matchbuoyvar=np.hstack([matchbuoyvar, buoyv]) 
#                datettimeww3b=np.hstack([datettimeww3b, buoyydate]) 

#                idxarray=np.hstack([idxarray, closest_idx])

#            else:
#                pass


#############################################################################################################################
    print matchmodelvar
    print matchbuoyvar

    np.save(''+savearraypath+'2'+vari+'_w_'+tname+'', matchmodelvar)
    np.save(''+savearraypath+'2time_w_'+tname+'', datettimeww3w)

    np.save(''+savearraypath+'2datetime_w_'+tname+'', datesww3w)

    np.save(''+savearraypath+'2'+vari+'_b_'+tname+'', matchbuoyvar)
    np.save(''+savearraypath+'2idxarray_b_'+tname+'', idxarray)



