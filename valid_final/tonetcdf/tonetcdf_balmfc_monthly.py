#! /usr/bin/env python26
#-*- coding: utf-8 -*-
#2/2014, Olga Vähä-Piikkiö


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


#case='balmfc'
case='balmfc_uerra'
#case='balmfc_era5'
#case='balmfc_v5'
#case='balmfc_era5_bm1.3'


if case=='balmfc':

    wampath='/home/vahapiik/BALMFC/WAM/files2019/'
    targetpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC/WAM/'

    yearmonth=['201601', '201602', '201603', '201604', '201605', '201606', '201607', '201608', '201609', '201610', '201611', '201612', '201701', '201702', '201703', '201704', '201705', '201706', '201707', '201708', '201709', '201710', '201711', '201712'] 


    prefix='BALMFC'


elif case=='balmfc_v5':

    wampath='/home/vahapiik/BALMFC/WAM/2018/Time_balmfc_v5_currents/'
    targetpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_v5/WAM/'

    yearmonth=['201801', '201802', '201803', '201804', '201805', '201806', '201807', '201808', '201809', '201810', '201811', '201812'] 


    prefix='BALMFC_v5'



elif case=='balmfc_uerra':

    wampath='/home/vahapiik/BALMFC/WAM/2018/Time_UERRA/'
    targetpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_UERRA/WAM/'

    yearmonth=['201801', '201802', '201803', '201804', '201805', '201806', '201807', '201808', '201809', '201810', '201811', '201812'] 

    prefix='BALMFC_UERRA'


elif case=='balmfc_era5':

    wampath='/home/vahapiik/BALMFC/WAM/2018/Time_ERA5/'
    targetpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5/WAM/'

    yearmonth=['201801', '201802', '201803', '201804', '201805', '201806', '201807', '201808', '201809', '201810', '201811', '201812'] 

    prefix='BALMFC_ERA5'


elif case=='balmfc_era5_bm1.3':

    wampath='/home/vahapiik/BALMFC/WAM/2018/Time_ERA5_bm1.3/'
    targetpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5_bm1.3/WAM/'

    yearmonth=['201801', '201802', '201803', '201804', '201805', '201806', '201807', '201808', '201809', '201810', '201811', '201812'] 

    prefix='BALMFC_ERA5_bm1.3'



#yerrrr=np.empty([0])
#monnnn=np.empty([0])
#dayyyy=np.empty([0])
#timmmm=np.empty([0])


#yearmonth=['201601', '201602', '201603', '201604', '201605', '201606', '201607', '201608', '201609', '201610', '201611', '201612', '201701', '201702', '201703', '201704', '201705', '201706', '201707', '201708', '201709', '201710', '201711', '201712'] 

#yearmonth=['201801', '201802', '201803', '201804', '201805', '201806', '201807', '201808', '201809', '201810', '201811', '201812'] 

#yr=2012
#yrmon=12
#buoy='HELS'

#buoyfilelist=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']
#frombuoyfilelist=['HKI', 'NBP', 'BB', 'BS', 'Arkona', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']

#buoyfilelist=['HelsinkiBuoy']
#frombuoyfilelist=['HKI']


buoyfilelist=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']
frombuoyfilelist=['HKI', 'NBP', 'BB', 'BS', 'HuvudskarOst', 'Arkona', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']



#buoy='HKI'
#buoy='NBP'
#buoy='BB'
#buoy='BS'

def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60




for buoy, fbuoy in zip(buoyfilelist, frombuoyfilelist):
    for yrmon in yearmonth:



        bettime=np.empty([0])


        try:

            c_HELS=subprocess.Popen(['ls -d '+wampath+'Time_'+str(yrmon)+'_'+fbuoy+''], shell=True, stdout=subprocess.PIPE)
        except IOError as e:
            continue
        print c_HELS
        newest_HELS=c_HELS.communicate()[0].strip()

        try:
            newesta_HELS=open(newest_HELS, 'r')
        except IOError as e:
            continue



        per_row_HELS = []
#        if line.startswith('  '+yrmon+''):
        for line in newesta_HELS:
            if line.startswith('  '+yrmon+''):
#                num_lines = sum(1 for line in open(newest_HELS, 'r'))
                per_row_HELS.append(line.strip().split())
            else:
                pass


#timest_hels=np.zeros((0,1), dtype='str')
#time_hels=np.zeros((0,1), dtype='float')

        per_column_t = zip(*per_row_HELS)

        timesss=np.array(per_column_t[0], dtype='str')
#mon_HELSb=np.array(per_column_HELS[0], dtype='str')
#day_HELSb=np.array(per_column_HELS[1], dtype='str')
#time_HELSb=np.array(per_column_HELS[2], dtype='str')
#filler1=np.array(per_column_HELS[3], dtype='float')
#filler2=np.array(per_column_HELS[4], dtype='float')


        wheight=np.array(per_column_t[9], dtype='float')
        pperiod=np.array(per_column_t[10], dtype='float')
        period=np.array(per_column_t[11], dtype='float')
        wdir2_t=np.array(per_column_t[14], dtype='float')
#        wdir22_t=np.array(per_column_t[14], dtype='float')



        wdir3_t=np.zeros((0,1), dtype='float')


        for r in wdir2_t:

            noopr=r+float(180)
            if noopr>=360:
                noop=noopr-float(360)
            elif noopr<0:
                noop=noopr+float(360)
            else:
                noop=noopr

            wdir3_t=np.vstack([wdir3_t, noop])


#        num_lines = sum(1 for line in open(newest_t, 'r'))




        wdir_t=np.reshape(wdir3_t,len(wheight)) 






#wherehs=np.where(mon_HELSb=='-9')


#pppp=0
      
#while pppp<len(wherehs):
#    filler1=np.delete(filler1, wherehs[pppp]-pppp)
#    filler2=np.delete(filler2, wherehs[pppp]-pppp)
#    wheightb=np.delete(wheightb, wherehs[pppp]-pppp)
#    pperiodb=np.delete(pperiodb, wherehs[pppp]-pppp)
#    wdirb=np.delete(wdirb, wherehs[pppp]-pppp)




#    pppp=pppp+1




#year_H=np.full(num_lines, yr)
#yr_H=np.full(num_lines, yrmon)

#print year_H
#print yr_H
######################################################################################



#yr_HELS=yr_H.astype(str)
#year_HELS=year_H.astype(str)






#for idx, (year_HEL, mon_HEL, day_HEL, time_HEL) in enumerate(zip(year_HELS, mon_HELSb, day_HELSb, time_HELSb)):
        for idx, tims in enumerate(timesss):

#    if mon_HEL=='-9':
#        print'hstuvregsyeytbvscwg'
#        pass
#    else:

#    if buoy=='HELS':
#        if (yrmon==16 and buoy=='HKI') or (yrmon==16 and buoy=='BB') or (yrmon==16 and buoy=='BS') or (yrmon=='2017a' and buoy=='BS'):

#    timestampp=datetime.datetime(int(tims[0:4]), int(tims[4:6]), int(tims[6:8]), int(tims[8:10]), int(tims[10:12]))-datetime.timedelta(hours=2)
            timestampp=datetime.datetime(int(tims[0:4]), int(tims[4:6]), int(tims[6:8]), int(tims[8:10]), int(tims[10:12]))

#    else:
#        timestampp=datetime.datetime(int(yr), int(mon_HEL), int(day_HEL), int(time_HEL[0:2]), int(time_HEL[3:5]))


#        tim=datetime.timedelta(days=1).total_seconds
#        print tim
#        tim=timestampp-datetime.datetime(1950,1,1)
#        print tim

#        timestamp=((timestampp-datetime.datetime(1950,1,1)).total_seconds)/ (datetime.timedelta(days=1).total_seconds)

            timestamp=(timestampp-datetime.datetime(1990,1,1)).total_seconds()  
#            timestamp=(timestampp-datetime.datetime(1950,1,1)).total_seconds()  
            timestamp=timestamp/(60*60*24)      
            print timestamp
#        timestamp=''+str(timestampp.strftime('%Y'))+'-'+str(timestampp.strftime('%m'))+'-'+str(timestampp.strftime('%d'))+' '+str(timestampp.strftime('%H.%M'))+':00'


            bettime=np.hstack([bettime, timestamp])
       
        print bettime[6]
        print bettime[7]



#        print filler1
#        print filler2
#        print type(wheight[9])
#        print type(bettime[9])
#        print wfreq2
        print wdir_t


#if buoy=='HKI':
#        if buoy=='HELS':
#            namb='HelsinkiBuoy'
#        elif buoy=='NBP':
#            namb='NorthernBaltic'
#        elif buoy=='BB':
#            namb='BothnianBay'
#        elif buoy=='BS':
#            namb='BothnianSea'

#g=Dataset('/home/vahapiik/BALMFC_2017_BUOYS/'+namb+'/BO_'+str(yr)+str(mon_HELSb[0])+'_TS_MO_'+namb+'.nc','w',format="NETCDF3_CLASSIC") # w if for
        g=Dataset(''+targetpath+prefix+'_'+str(yrmon)+'_'+buoy+'.nc','w',format="NETCDF3_CLASSIC") # w if for creating a file


        g.createDimension('TIME',len(bettime))
#g.createDimension('timestamp',32)



        dims=('TIME')


#bettime=netCDF4.stringtochar(bettime)
        print np.shape(bettime)

        var1 = g.createVariable('time','float',dims,fill_value=-999)
        var2 = g.createVariable('hs','float',dims,fill_value=-999)
        var3 = g.createVariable('fp','float',dims,fill_value=-999)
        var4 = g.createVariable('t02','float',dims,fill_value=-999)
        var5 = g.createVariable('wdir','float',dims,fill_value=-999)



        var1[:] = bettime[:]

        var2[:] = wheight[:]        

        var3[:] = pperiod[:]

        var4[:] = period[:]

        var5[:] = wdir_t[:]

        g.close()

