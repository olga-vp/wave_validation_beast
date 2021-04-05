#! /usr/bin/env python26
#-*- coding: utf-8 -*-
#4/2019, Olga Vähä-Piikkiö


import numpy as np
import netCDF4
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
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




bettime=np.empty([0])
stringtime=np.empty([0])


yerrrr=np.empty([0])
monnnn=np.empty([0])
dayyyy=np.empty([0])
timmmm=np.empty([0])

yr=2013
yrmon=13

#buoy='HKI'
#buoy='NBP'
#buoy='BB'
buoy='BS'
buoy='PERM'

utceet='ei'


c_HELS=subprocess.Popen(['ls -d '+buoy+str(yrmon)+'.SUU'], shell=True, stdout=subprocess.PIPE)

newest_HELS=c_HELS.communicate()[0].strip()

newesta_HELS=open(newest_HELS, 'r')


num_lines = sum(1 for line in open(newest_HELS, 'r'))

per_row_HELS = []
for idx, line in enumerate(newesta_HELS):

    if idx==0:
        if ('EET' in line) or ('eet' in line):
            utceet='EET'
        elif ('UTC' in line) or ('utc' in line):
            utceet='UTC' 
        else:
            utceet='assume UTC'
        
    else:

        per_row_HELS.append(line.strip().split())



timest_hels=np.zeros((0,1), dtype='str')
time_hels=np.zeros((0,1), dtype='float')

per_column_HELS = zip(*per_row_HELS)


mon_HELSb=np.array(per_column_HELS[0], dtype='str')
day_HELSb=np.array(per_column_HELS[1], dtype='str')
time_HELSb=np.array(per_column_HELS[2], dtype='str')
filler1=np.array(per_column_HELS[3], dtype='float')
filler2=np.array(per_column_HELS[4], dtype='float')
wheightb=np.array(per_column_HELS[5], dtype='float')

wfreq2=np.array(per_column_HELS[6], dtype='float')
pperiodb=1/wfreq2

wdirb=np.array(per_column_HELS[7], dtype='float')


#wfreq3=np.zeros((0,1), dtype='float')


#for x in wfreq2:

#    noop=float(1)/x 
#    wfreq3=np.vstack([wfreq3, noop])

#pperiodb=np.reshape(wfreq3,num_lines) 
    





wherehs=np.where(mon_HELSb=='-9')


pppp=0
      
while pppp<len(wherehs):
    filler1=np.delete(filler1, wherehs[pppp]-pppp)
    filler2=np.delete(filler2, wherehs[pppp]-pppp)
    wheightb=np.delete(wheightb, wherehs[pppp]-pppp)
    pperiodb=np.delete(pperiodb, wherehs[pppp]-pppp)
    wdirb=np.delete(wdirb, wherehs[pppp]-pppp)




    pppp=pppp+1




year_H=np.full(num_lines, yr)
yr_H=np.full(num_lines, yrmon)

print year_H
print yr_H
######################################################################################



yr_HELS=yr_H.astype(str)
year_HELS=year_H.astype(str)



def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60


for idx, (year_HEL, mon_HEL, day_HEL, time_HEL) in enumerate(zip(year_HELS, mon_HELSb, day_HELSb, time_HELSb)):



    if mon_HEL=='-9':
        print'hstuvregsyeytbvscwg'
        pass
    else:


        if utceet=='EET':
            print 'EET'
            timestampp=datetime.datetime(int(yr), int(mon_HEL), int(day_HEL), int(time_HEL[0:2]), int(time_HEL[3:5]))-datetime.timedelta(hours=2)

        elif utceet=='UTC':  
            print 'UTC'
            timestampp=datetime.datetime(int(yr), int(mon_HEL), int(day_HEL), int(time_HEL[0:2]), int(time_HEL[3:5]))
        else:
            print 'assume UTC'
            timestampp=datetime.datetime(int(yr), int(mon_HEL), int(day_HEL), int(time_HEL[0:2]), int(time_HEL[3:5]))




        timestamp=(timestampp-datetime.datetime(1950,1,1)).total_seconds()  
        timestamp=timestamp/(60*60*24)      
        print timestamp

        timestring=''+str(timestampp.strftime('%Y'))+'-'+str(timestampp.strftime('%m'))+'-'+str(timestampp.strftime('%d'))+' '+str(timestampp.strftime('%H.%M'))+':00'

        bettime=np.hstack([bettime, timestamp])
        stringtime=np.hstack([stringtime, timestring])
       
print bettime[6]
print bettime[7]



print filler1
print filler2
print type(wheightb[9])
print type(bettime[9])
print wfreq2
print wdirb



if buoy=='HKI':
    namb='HelsinkiBuoy'
elif buoy=='NBP':
    namb='NorthernBaltic'
elif buoy=='BB':
    namb='BothnianBay'
elif buoy=='BS':
    namb='BothnianSea'
elif buoy=='PERM':
    namb='BothnianBay'

#g=Dataset('/home/vahapiik/BALMFC_2017_BUOYS/'+namb+'/BO_'+str(yr)+str(mon_HELSb[0])+'_TS_MO_'+namb+'.nc','w',format="NETCDF3_CLASSIC") # w if for creating a file
g=Dataset('BO_'+str(yr)+str(mon_HELSb[0])+'_TS_MO_'+namb+'.nc','w',format="NETCDF3_CLASSIC") # w if for creating

g.createDimension('TIME',len(timmmm))
g.createDimension('timestring',32)



dims=('TIME')


stringtime=netCDF4.stringtochar(stringtime)
print np.shape(bettime)

var1 = g.createVariable('TIME','float',dims,fill_value=-999)
var2 = g.createVariable('TIMESTAMP','S1',('TIME','timestring'),fill_value=-999)
var3 = g.createVariable('VHM0','float',dims,fill_value=-999)
var4 = g.createVariable('VTPK','float',dims,fill_value=-999)
var5 = g.createVariable('VPED','float',dims,fill_value=-999)



var1[:] = bettime[:]

var2[:] = stringtime[:]

var3[:] = wheightb[:]        

var4[:] = pperiodb[:]

var5[:] = wdirb[:]

g.close()

