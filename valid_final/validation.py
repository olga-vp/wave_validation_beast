#! /usr/bin/env python
#-*- coding: utf-8 -*-
#2/2019, Olga Vähä-Piikkiö


import os
import sys
import subprocess


monthly=0


#pick one of these or make your own
#possible modes:
#mode='balmfc'
#mode='sats'
#mode='ww3_valid_hels'
mode='winds'
#mode='argo'
#mode='balmfc_era5'
#mode='balmfc_era5_bm1.3'
#mode='balmfc_uerra'
#mode='balmfc_v5'

#monthly=12



#possible cases:
#timeseries from one lat lon point 
#case='1point'
#timeseries in a file containing multiple locations
#case='pick1point'
#observed timeseries moving in space, this picks the closest point in the model for every moment  
#case='moving'

###################################################################################################################################################################

if mode=='balmfc':

    case='1point'  

    lonn='dummy'
    latt='dummy'

    variable=['wheight','pperiod','period'] 

    buoyfilelist=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']
    buoyorigin=['cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems']

#    dirlist = ['BO_TS_MO_HelsinkiBuoy.nc', 'BO_TS_MO_NorthernBaltic.nc', 'BO_TS_MO_BothnianBay.nc', 'BO_TS_MO_BothnianSea.nc','BO_TS_MO_HuvudskarOst.nc', 'BO_TS_MO_ArkonaWR.nc', 'BO_TS_MO_VaderoarnaWR.nc', 'BO_TS_MO_FinngrundetWR.nc', 'BO_TS_MO_DarsserSWR.nc']

    yearmonth=['201601', '201602', '201603', '201604', '201605', '201606', '201607', '201608', '201609', '201610', '201611', '201612', '201701', '201702', '201703', '201704', '201705', '201706', '201707', '201708', '201709', '201710', '201711', '201712'] 



    buoyfilelist_wheight_allbuoys=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']
#    dirlist_wheight_allbuoys = ['BO_TS_MO_HelsinkiBuoy.nc', 'BO_TS_MO_NorthernBaltic.nc', 'BO_TS_MO_BothnianBay.nc', 'BO_TS_MO_BothnianSea.nc','BO_TS_MO_HuvudskarOst.nc', 'BO_TS_MO_ArkonaWR.nc', 'BO_TS_MO_VaderoarnaWR.nc', 'BO_TS_MO_FinngrundetWR.nc', 'BO_TS_MO_DarsserSWR.nc']

    buoyfilelist_pperiod_allbuoys=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'FinngrundetWR']
#    dirlist_pperiod_allbuoys = ['BO_TS_MO_HelsinkiBuoy.nc', 'BO_TS_MO_NorthernBaltic.nc', 'BO_TS_MO_BothnianBay.nc', 'BO_TS_MO_BothnianSea.nc', 'BO_TS_MO_HuvudskarOst.nc', 'BO_TS_MO_ArkonaWR.nc', 'BO_TS_MO_FinngrundetWR.nc']

    buoyfilelist_period_allbuoys=['ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']
#    dirlist_period_allbuoys = ['BO_TS_MO_ArkonaWR.nc', 'BO_TS_MO_VaderoarnaWR.nc', 'BO_TS_MO_FinngrundetWR.nc', 'BO_TS_MO_DarsserSWR.nc']


    prefix='BALMFC_'
    plotfix=''

    wampath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC/WAM'
    buoypath='/home/vahapiik/BALMFC_2017_BUOYS'
    arraypath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC/arrays2019/'
    arraypath2='/media/vahapiik/My_Passport/validaatio/cases/BALMFC/arrays2019/text'
    saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC/plots2019/'
    statpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC/stats/'




##############################################################################################################################################################################


elif mode=='balmfc_v5':

    case='1point'  

    lonn='dummy'
    latt='dummy'

    variable=['wheight','pperiod','period'] 
#    variable=['pperiod'] 

    buoyfilelist=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']
    buoyorigin=['cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems']


#    buoyfilelist=['HelsinkiBuoy']
#    buoyorigin=['cmems']


    yearmonth=['201801', '201802', '201803', '201804', '201805', '201806', '201807', '201808', '201809', '201810', '201811', '201812'] 
#    yearmonth=['201812'] 


    buoyfilelist_wheight_allbuoys=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']


    buoyfilelist_pperiod_allbuoys=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'FinngrundetWR']


    buoyfilelist_period_allbuoys=['ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']



    prefix='BALMFC_v5_'
#    plotfix='_v5_12'
    plotfix='_v5'

    wampath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_v5/WAM'
    buoypath='/home/vahapiik/BALMFC_2017_BUOYS'
    arraypath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_v5/arrays/'
    arraypath2='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_v5/arrays/text'
    saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_v5/plots/'
#    saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_v5/plots/12/'
    statpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_v5/stats/'


    if monthly==12:
        
        yearmonth=['201812'] 
        plotfix='_v5_12'
        saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_v5/plots/12/'
        statpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_v5/stats/12/'


##############################################################################################################################################################################


elif mode=='balmfc_uerra':

    case='1point'  

    lonn='dummy'
    latt='dummy'

    variable=['wheight','pperiod','period'] 
#    variable=['pperiod'] 

#    buoyfilelist=['HuvudskarOst', 'ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']
#    buoyorigin=['cmems', 'cmems', 'cmems', 'cmems', 'cmems']



    buoyfilelist=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']
    buoyorigin=['cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems']


#    buoyfilelist=['HuvudskarOst']
#    buoyorigin=['cmems']

    yearmonth=['201801', '201802', '201803', '201804', '201805', '201806', '201807', '201808', '201809', '201810', '201811', '201812'] 
#    yearmonth=['201812'] 


    buoyfilelist_wheight_allbuoys=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']
    buoyfilelist_pperiod_allbuoys=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'FinngrundetWR']
    buoyfilelist_period_allbuoys=['ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']


    prefix='BALMFC_UERRA_'
    plotfix='_UERRA'
#    plotfix='_UERRA_12'
    

    wampath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_UERRA/WAM'
    buoypath='/home/vahapiik/BALMFC_2017_BUOYS'
    arraypath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_UERRA/arrays/'
    arraypath2='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_UERRA/arrays/text'
    saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_UERRA/plots/'
#    saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_UERRA/plots/12/'
    statpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_UERRA/stats/'


    if monthly==12:
        
        yearmonth=['201812'] 
        plotfix='_UERRA_12'
        saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_UERRA/plots/12/'
        statpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_UERRA/stats/12/'

##############################################################################################################################################################################


elif mode=='balmfc_era5':

    case='1point'  

    lonn='dummy'
    latt='dummy'

    variable=['wheight','pperiod','period'] 
#    variable=['pperiod'] 

    buoyfilelist=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']
    buoyorigin=['cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems']


#    buoyfilelist=['ArkonaWR']
#    buoyorigin=['cmems']


    yearmonth=['201801', '201802', '201803', '201804', '201805', '201806', '201807', '201808', '201809', '201810', '201811', '201812'] 
#    yearmonth=['201812']


    buoyfilelist_wheight_allbuoys=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']
    buoyfilelist_pperiod_allbuoys=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'FinngrundetWR']
    buoyfilelist_period_allbuoys=['ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']


    prefix='BALMFC_ERA5_'
#    plotfix='_ERA5_12'
    plotfix='_ERA5'

    wampath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5/WAM'
    buoypath='/home/vahapiik/BALMFC_2017_BUOYS'
    arraypath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5/arrays/'
    arraypath2='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5/arrays/text'
    saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5/plots/'
#    saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5/plots/12/'
    statpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5/stats/'

    if monthly==12:
        
        yearmonth=['201812'] 
        plotfix='_ERA5_12'
        saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5/plots/12/'
        statpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5/stats/12/'


##############################################################################################################################################################################


elif mode=='balmfc_era5_bm1.3':

    case='1point'  

    lonn='dummy'
    latt='dummy'

    variable=['wheight','pperiod','period'] 
#    variable=['pperiod'] 

    buoyfilelist=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'ArkonaWR', 'HuvudskarOst', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']
    buoyorigin=['cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems', 'cmems']


#    buoyfilelist=['HelsinkiBuoy']
#    buoyorigin=['cmems']


    yearmonth=['201801', '201802', '201803', '201804', '201805', '201806', '201807', '201808', '201809', '201810', '201811', '201812'] 
#    yearmonth=['201812']


    buoyfilelist_wheight_allbuoys=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']
    buoyfilelist_pperiod_allbuoys=['HelsinkiBuoy', 'NorthernBaltic', 'BothnianBay', 'BothnianSea', 'HuvudskarOst', 'ArkonaWR', 'FinngrundetWR']
    buoyfilelist_period_allbuoys=['ArkonaWR', 'VaderoarnaWR', 'FinngrundetWR', 'DarsserSWR']


    prefix='BALMFC_ERA5_bm1.3_'
#    plotfix='_ERA5_bm1.3_12'
    plotfix='_ERA5_bm1.3'

    wampath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5_bm1.3/WAM'
    buoypath='/home/vahapiik/BALMFC_2017_BUOYS'
    arraypath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5_bm1.3/arrays/'
    arraypath2='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5_bm1.3/arrays/text'
    saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5_bm1.3/plots/'
#    saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5_bm1.3/plots/12/'
    statpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5_bm1.3/stats/'

    if monthly==12:
        
        yearmonth=['201812'] 
        plotfix='_ERA5_bm1.3_12'
        saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5_bm1.3/plots/12/'
        statpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_ERA5_bm1.3/stats/12/'

############################################################################################################################################################################

elif mode=='sats':

    case='1point'

    lonn='dummy'
    latt='dummy'

    variable=['wheight']

    buoyfilelist=['SWH_wam_al', 'SWH_wam_j3', 'SWH_wam_s3a']
    buoyorigin=['other', 'other', 'other']

#    dirlist = ['BO_TS_MO_SWH_wam_al.nc', 'BO_TS_MO_SWH_wam_j3.nc', 'BO_TS_MO_SWH_wam_s3a.nc']

    yearmonth=['201601', '201602', '201603', '201604', '201605', '201606', '201607', '201608', '201609', '201610', '201611', '201612', '201701', '201702', '201703', '201704', '201705', '201706', '201707', '201708', '201709', '201710', '201711', '201712']

    buoyfilelist_wheight_allbuoys=['al', 'jason', 'sentinel']
#    dirlist_wheight_allbuoys = ['BO_TS_MO_SWH_wam_al.nc', 'BO_TS_MO_SWH_wam_j3.nc', 'BO_TS_MO_SWH_wam_s3a.nc']

    prefix=''
    plotfix=''

    wampath='/home/vahapiik/BALMFC/WAM/files2019'
    buoypath='/home/vahapiik/BALMFC_2017_BUOYS/sats'
    arraypath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_sats/arrays2019/'
    arraypath2='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_sats/arrays2019/text'
    saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_sats/plots2019/'
    statpath='/media/vahapiik/My_Passport/validaatio/cases/BALMFC_sats/stats/'

###############################################################################################################################################################################

elif mode=='ww3_valid_hels':

    case='pick1point'

    #HELS
    lonn='25.235166667'
    latt='59.965'

#    variable=['wheight','pperiod']
#    variable=['pperiod']
    variable=['wdir']

#    variable=['wdir','wheight','pperiod']

    buoyfilelist=['HelsinkiBuoy']
    buoyorigin=['other']
#    dirlist = ['BO_TS_MO_HelsinkiBuoy.nc']

#    yearmonth=['201009']

    yearmonth=['201001','201002','201003','201004', '201005', '201006', '201007', '201008', '201009', '201010', '201011','201012','201101','201102','201103', '201104', '201105', '201106', '201107', '201108', '201109', '201110', '201111','201112', '201201','201202','201203','201204', '201205', '201206', '201207', '201208', '201209', '201210', '201211','201212']



    prefix='ww3.'
    plotfix='ww3'

#    wampath='/media/vahapiik/My_Passport/ww3_validation/ww3'
    wampath='/media/vahapiik/My_Passport/wavewatch_mypassport/2010_11_12/direct'
#    wampath='/media/vahapiik/My_Passport/wavewatch_mypassport/2010_11_12'
    buoypath='/media/vahapiik/My_Passport/validaatio/cases/WW3/buoys'
    arraypath='/media/vahapiik/My_Passport/validaatio/cases/WW3/arrays/'
    arraypath2='/media/vahapiik/My_Passport/validaatio/cases/WW3/arrays/text'
    saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/WW3/plots/'
    statpath='/media/vahapiik/My_Passport/validaatio/cases/WW3/stats/'


###################################################################################################################################################################################

elif mode=='winds':

    case='pick1point'

    #KALB
    lonn='25.59861111'
    latt='59.98555555'

    variable=['windmag', 'winddir']
#    variable=['winddir']

#    buoyfilelist=['BO_TS_MO_Kalbadagrund.nc']
    buoyfilelist=['Kalbadagrund']
    buoyorigin=['other']

#    yearmonth=['201001','201002','201003','201004', '201005', '201006','201007']

#    yearmonth=['201009']

    yearmonth=['201001','201002','201003','201004', '201005', '201006', '201007', '201008', '201009', '201010', '201011','201012','201101','201102','201103', '201104', '201105', '201106', '201107', '201108', '201109', '201110', '201111','201112', '201201','201202','201203','201204', '201205', '201206', '201207', '201208', '201209', '201210', '201211','201212']

    prefix='ww3.'
    plotfix='wind'


    wampath='/media/vahapiik/My_Passport/ww3_validation/ww3'
    buoypath='/media/vahapiik/My_Passport/validaatio/cases/winds_ww3/buoy'
    arraypath='/media/vahapiik/My_Passport/validaatio/cases/winds_ww3/arrays/'
    arraypath2='/media/vahapiik/My_Passport/validaatio/cases/winds_ww3/arrays/text'
    saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/winds_ww3/plots/'
    statpath='/media/vahapiik/My_Passport/validaatio/cases/winds_ww3/stats/'


#############################################################################################################################################################################

elif mode=='argo':

    case='moving'
    
    lonn='dummy'
    latt='dummy'

    variable=['wheight','pperiod'] 

#    buoyfilelist=['BAB3','SIS1']
#    buoyorigin=['other','other']

    buoyfilelist=['BAB1','BAB3','SIS1']
    buoyorigin=['other','other','other']


    yearmonth=['201009', '201010', '201011','201012','201101','201102','201103', '201104', '201105', '201106', '201107', '201108', '201109', '201110', '201111','201112', '201201','201202','201203','201204', '201205', '201206', '201207', '201208', '201209']



    prefix='ww3.'
    plotfix='_ww3'

    wampath='/media/vahapiik/My_Passport/ww3_validation/ww3'
    buoypath='/media/vahapiik/My_Passport/validaatio/cases/argo/buoy'
    arraypath='/media/vahapiik/My_Passport/validaatio/cases/argo/arrays/'
    arraypath2='/media/vahapiik/My_Passport/validaatio/cases/argo/arrays/text'
    saveplotpath='/media/vahapiik/My_Passport/validaatio/cases/argo/plots/'
    statpath='/media/vahapiik/My_Passport/validaatio/cases/argo/stats/'





############################################################################################################################################################################

#print buoyfilelist[0]

#j=0
#while j<len(buoyfilelist):
#    buoyf=buoyfilelist[j]
#    i=0
#    while i<len(variable):
#        vari=variable[i]
##        print vari
#        print buoyf
##        print len(buoyfilelist)
#        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/matching.py %s %s %s %s %s %s %s %s %s %s" %(buoyf, ''+prefix+'', vari,''+wampath+'',''+buoypath+'',''+arraypath+'',''+case+'',''+lonn+'',''+latt+'',yearmonth))
#        i=i+1
#    j=j+1




#j=0

#while j<len(buoyfilelist):
#    buoyf=buoyfilelist[j]
#    orig=buoyorigin[j]
#    print buoyf
##    dirl=dirlist[j]
#    i=0
#    while i<len(variable):
#        vari=variable[i]
#        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/stats.py>>"+statpath+"stats_%s.txt %s %s %s %s %s %s %s %s" %(buoyf,buoyf,orig,''+prefix+'', vari,''+arraypath2+'',''+buoypath+'',''+arraypath+'',yearmonth))

##        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/stats.py %s %s %s %s %s %s %s %s" %(buoyf,orig,''+prefix+'', vari,''+arraypath2+'',''+buoypath+'',''+arraypath+'',yearmonth))

#        i=i+1
#    j=j+1


j=0

while j<len(buoyfilelist):
    buoyf=buoyfilelist[j]
#    dirl=dirlist[j]
    i=0
    while i<len(variable):
        vari=variable[i]
#        if buoyf=='HelsinkiBuoy' or buoyf=='NorthernBaltic' or buoyf=='BothnianBay' or buoyf=='BothnianSea':
        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/plot.py %s %s %s %s %s %s %s %s" %(buoyf, ''+prefix+'',''+plotfix+'',vari,''+saveplotpath+'',''+buoypath+'',''+arraypath+'',yearmonth))

        i=i+1
    j=j+1




i=0
while i<len(variable):
    vari=variable[i]
    if vari=='wheight':
        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/plot_all.py %s %s %s %s" %(vari,''+saveplotpath+'',''+arraypath+'',buoyfilelist_wheight_allbuoys))
        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/stats_all.py>>'+statpath+'stats_wheight_allbuoys.txt %s %s %s" %(vari,''+arraypath+'',buoyfilelist_wheight_allbuoys))

    elif vari=='pperiod':
        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/plot_all.py %s %s %s %s" %(vari,''+saveplotpath+'',''+arraypath+'',buoyfilelist_pperiod_allbuoys))
        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/stats_all.py>>'+statpath+'stats_pperiod_allbuoys.txt %s %s %s" %(vari,''+arraypath+'',buoyfilelist_pperiod_allbuoys))

    elif vari=='period':
        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/plot_all.py %s %s %s %s" %(vari,''+saveplotpath+'',''+arraypath+'',buoyfilelist_period_allbuoys))
        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/stats_all.py>>'+statpath+'stats_period_allbuoys.txt %s %s %s" %(vari,''+arraypath+'',buoyfilelist_period_allbuoys))

    elif vari=='windmag':
        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/plot_all.py %s %s %s %s" %(vari,''+saveplotpath+'',''+arraypath+'',buoyfilelist_windmag_allbuoys))
        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/stats_all.py>>'+statpath+'stats_windmag_allbuoys.txt %s %s %s" %(vari,''+arraypath+'',buoyfilelist_windmag_allbuoys))

    elif vari=='winddir':
        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/plot_all.py %s %s %s %s" %(vari,''+saveplotpath+'',''+arraypath+'',buoyfilelist_winddir_allbuoys))
        os.system("/media/vahapiik/My_Passport/validaatio/scripts/sub/stats_all.py>>'+statpath+'stats_winddir_allbuoys.txt %s %s %s" %(vari,''+arraypath+'',buoyfilelist_winddir_allbuoys))

    i=i+1
