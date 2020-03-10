#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:43:50 2020

@author: lp555
"""

#%% In the future write below as a function to save time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import pymannkendall as mk
#%% import multiple csv files and concatenate them into one single dataframe - take notes!  
#df = pd.concat(map(pd.read_csv, glob.glob(os."/home/lp555/Beijing/Observations/Sinaapp/data/Beijing_2014_to_2019".join('', "*.csv")))) - good one liner but takes time to figure out how it really works
path = r'/home/lp555/Beijing/Observations/Sinaapp/data/Beijing_O3_2014_to_2019'
#files = glob.glob(path + "/*.csv") - good but can be improved
O3_files = glob.glob(os.path.join(path, "*.csv"))
df_O3 = pd.concat((pd.read_csv(f) for f in O3_files))
df_O3.columns = ['Date','pollutant', 'DS','TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ','ZWY', 'FTHY', 'YG', 'GC', 'FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ', 'DL', 'BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH', 'QM', 'YDMN', 'XZMB', 'NSH', 'DSH']
#%% Wanliu Daily Mean
df_O3.Date = pd.to_datetime(df_O3.Date, dayfirst = True)
df_O3.sort_values(by=['Date'], inplace = True)
beijing_O3 = df_O3.set_index('Date')
del beijing_O3['pollutant']
beijing_O3 = beijing_O3/2 # to convert ug/m3 to ppb
#%%
wl_O3 = beijing_O3.WL
wl_O3 = pd.DataFrame(wl_O3)
wl_O3_dm = wl_O3.resample('D').mean()
wl_O3_dm.plot()
#%%
#beijing_O3.to_csv('/home/lp555/Beijing/Observations/Sinaapp/data/Beijing_O3_2014_to_2019/beijing_O3_all.csv')
#%% Wanliu Monthly mean of Daily mean
wl_O3_mmdm = wl_O3_dm.resample('M').mean()
wl_O3_mmdm.plot(marker = 'o')
#%%
mk_result_O3 = mk.seasonal_test(wl_O3_mmdm[9:], period = 12) # ignored the year 2014 or the increasing trend would be more significant
print(mk_result_O3)
#%%
#def station_dm(df_station):
    #df_station_dm = df_station.resample('D').mean() # convert to df before this
    #print(df_station_dm)
beijing_O3_dm = beijing_O3.resample('D').mean()
urban_dm = beijing_O3_dm.loc[:, 'DS':'GC']
suburban_dm = beijing_O3_dm.loc[: , 'FS':'YQ']
dl_dm = pd.DataFrame(beijing_O3_dm.loc[:, 'DL'])
regional_bg_dm = beijing_O3_dm.loc[:, 'BDL':'LLH']
traffic_dm = beijing_O3_dm.loc[:, 'QM':'DSH']
#beijing_O3_dm.plot(subplots = True, layout=(5,7), figsize = (6,9))
#%% see if need to set the axes with same values? BELOW dm for different types of stations
#fig, axes = plt.subplots(nrows = 4, ncols = 3)
#plt.title('Urban Stations Daily Mean', fontsize = 16)
#plt.legend(loc = 'upper left')
urban_dm.plot(subplots = True, layout = (4,3), legend = False, title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY','FTHY', 'YG', 'GC']) #, title = 'Urban Stations Daily Mean')
plt.suptitle('Urban Stations Daily Mean', fontsize = 16)
 # Draw the figure so you can find the positon of the legend. 

#fig, axes = plt.subplots(nrows = 4, ncols = 3)
suburban_dm.columns.values
suburban_dm.plot(subplots = True, layout = (4,3), title = ['FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ'])
plt.suptitle('Suburban Stations Daily Mean', fontsize = 16)

dl_dm.plot()
plt.suptitle('DingLing Daily Mean', fontsize = 16)

regional_bg_dm.columns.values
regional_bg_dm.plot(subplots = True, layout = (2,3), title = ['BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH'])
plt.suptitle('Regional Background Stations Daily Mean', fontsize = 16)

traffic_dm.columns.values
traffic_dm.plot(subplots = True, layout = (2,3), title = ['QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Traffic Stations Daily Mean', fontsize = 16)
#%%
beijing_O3_mmdm = beijing_O3_dm.resample('M').mean()
urban_mmdm = beijing_O3_mmdm.loc[:, 'DS':'GC']
suburban_mmdm = beijing_O3_mmdm.loc[: , 'FS':'YQ']
dl_mmdm = pd.DataFrame(beijing_O3_mmdm.loc[:, 'DL'])
regional_bg_mmdm = beijing_O3_mmdm.loc[:, 'BDL':'LLH']
traffic_mmdm = beijing_O3_mmdm.loc[:, 'QM':'DSH']
#%%
urban_mmdm.plot(subplots = True, layout = (4,3), legend = False, title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY','FTHY', 'YG', 'GC'], marker = 'o') #, title = 'Urban Stations Daily Mean')
plt.suptitle('Urban Stations Monthly Mean of Daily Mean', fontsize = 16)

suburban_mmdm.plot(subplots = True, layout = (4,3), marker = 'o', title = ['FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ'])
plt.suptitle('Suburban Stations Monthly Mean of Daily Mean', fontsize = 16)

dl_mmdm.plot(marker = 'o')
plt.suptitle('DingLing Monthly Mean of Daily Mean', fontsize = 16)

regional_bg_mmdm.plot(subplots = True, layout = (2,3), marker = 'o', title = ['BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH'])
plt.suptitle('Regional Background Stations Monthly Mean of Daily Mean', fontsize = 16)

traffic_mmdm.plot(subplots = True, layout = (2,3), marker = 'o', title = ['QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Traffic Stations Monthly Mean of Daily Mean', fontsize = 16)
#%% mda8
beijing_mda8 = (beijing_O3.rolling(8, min_periods = 6).mean()).resample('D').max()
urban_mda8 = beijing_mda8.loc[:, 'DS':'GC']
suburban_mda8 = beijing_mda8.loc[:, 'FS':'YQ']
dl_mda8 = pd.DataFrame(beijing_mda8.loc[:, 'DL'])
regional_bg_mda8 = beijing_mda8.loc[:,'BDL':'LLH' ]
traffic_mda8 = beijing_mda8.loc[:, 'QM':'DSH']
#%% mda8
urban_mda8.plot(subplots = True, layout = (4,3), legend = False, title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY','FTHY', 'YG', 'GC']) #, title = 'Urban Stations Daily Mean')
plt.suptitle('Urban Stations MDA8', fontsize = 16)

suburban_mda8.plot(subplots = True, layout = (4,3),title = ['FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ'])
plt.suptitle('Suburban Stations MDA8', fontsize = 16)

dl_mda8.plot()
plt.suptitle('DingLing MDA8', fontsize = 16)

regional_bg_mda8.plot(subplots = True, layout = (2,3), title = ['BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH'])
plt.suptitle('Regional Background Stations MDA8', fontsize = 16)

traffic_mda8.plot(subplots = True, layout = (2,3), title = ['QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Traffic Stations MDA8', fontsize = 16)
#%% monthly mean of mda8
beijing_mmmda8 = beijing_mda8.resample('M').mean()
urban_mmmda8 = beijing_mmmda8.loc[:, 'DS':'GC']
suburban_mmmda8 = beijing_mmmda8.loc[:, 'FS':'YQ']
dl_mmmda8 = pd.DataFrame(beijing_mmmda8.loc[:, 'DL'])
regional_bg_mmmda8 = beijing_mmmda8.loc[:,'BDL':'LLH' ]
traffic_mmmda8 = beijing_mmmda8.loc[:, 'QM':'DSH']
#%%
urban_mmmda8.plot(subplots = True, layout = (4,3), legend = False, title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY','FTHY', 'YG', 'GC'], marker = 'o') #, title = 'Urban Stations Daily Mean')
plt.suptitle('Urban Stations Monthly Mean of MDA8', fontsize = 16)

suburban_mmmda8.plot(subplots = True, layout = (4,3), marker = 'o', title = ['FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ'])
plt.suptitle('Suburban Stations Monthly Mean of MDA8', fontsize = 16)

dl_mmmda8.plot(marker = 'o')
plt.suptitle('DingLing Monthly Mean of MDA8', fontsize = 16)

regional_bg_mmmda8.plot(subplots = True, layout = (2,3), marker = 'o', title = ['BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH'])
plt.suptitle('Regional Background Stations Monthly Mean of MDA8', fontsize = 16)

traffic_mmmda8.plot(subplots = True, layout = (2,3), marker = 'o', title = ['QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Traffic Stations Monthly Mean of MDA8', fontsize = 16)
#%% MDA1 
beijing_mda1 = beijing_O3.resample('D').max()
urban_mda1 = beijing_mda1.loc[:, 'DS':'GC']
suburban_mda1 = beijing_mda1.loc[:, 'FS':'YQ']
dl_mda1 = pd.DataFrame(beijing_mda1.loc[:, 'DL'])
regional_bg_mda1 = beijing_mda1.loc[:,'BDL':'LLH' ]
traffic_mda1 = beijing_mda1.loc[:, 'QM':'DSH']
#%%
urban_mda1.plot(subplots = True, layout = (4,3), legend = False, title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY','FTHY', 'YG', 'GC']) #, title = 'Urban Stations Daily Mean')
plt.suptitle('Urban Stations MDA1', fontsize = 16)

suburban_mda1.plot(subplots = True, layout = (4,3),title = ['FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ'])
plt.suptitle('Suburban Stations MDA1', fontsize = 16)

dl_mda1.plot()
plt.suptitle('DingLing MDA1', fontsize = 16)

regional_bg_mda1.plot(subplots = True, layout = (2,3), title = ['BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH'])
plt.suptitle('Regional Background Stations MDA1', fontsize = 16)

traffic_mda1.plot(subplots = True, layout = (2,3), title = ['QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Traffic Stations MDA1', fontsize = 16)
#%% 4MDA8
def fmda8(df_station):
    station_by_year = [group[1] for group in df_station.groupby(df_station.index.year)]
    mda8_4_station = []
    fmda8_station = []
    for df in station_by_year:
        values = df.nlargest(4)#, pd.DataFrame(df).columns[0])
        mda8_4_station.append(values)
    for df in mda8_4_station:
        value = df.nsmallest(1)#, pd.DataFrame(df).columns[0])
        fmda8_station.append(value)
    return(fmda8_station)
all_stats = []
for column in beijing_mda8:
    all_stat = fmda8(beijing_mda8[column])

    for row in all_stat:
        rows = pd.DataFrame(row)
        all_stats.append(rows)
realtest = pd.concat(all_stats, ignore_index = True, sort = False)

#%%
fmda8_all_stat = pd.read_csv('/home/lp555/Beijing/Observations/Sinaapp/data/4mda8_all_stat.csv', index_col = ['Year'])
urban_4mda8 = fmda8_all_stat.loc[:, 'DS':'GC']
suburban_4mda8 = fmda8_all_stat.loc[:, 'FS':'YQ']
dl_4mda8 = pd.DataFrame(fmda8_all_stat.loc[:, 'DL'])
regional_bg_4mda8 = fmda8_all_stat.loc[:,'BDL':'LLH' ]
traffic_4mda8 = fmda8_all_stat.loc[:, 'QM':'DSH']
#%%
urban_4mda8.plot(subplots = True, ylim = (80,155), layout = (4,3), marker = 'o', legend = False, title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY','FTHY', 'YG', 'GC']) #, title = 'Urban Stations Daily Mean')

suburban_4mda8.plot(subplots = True,ylim = (100,200),marker = 'o', layout = (4,3),title = ['FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ'])
plt.suptitle('Suburban Stations 4MDA8', fontsize = 16)

dl_4mda8.plot(marker = 'o',ylim = (100,200),)
plt.suptitle('DingLing 4MDA8', fontsize = 16)

regional_bg_4mda8.plot(subplots = True,ylim = (100,200),marker = 'o', layout = (2,3), title = ['BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH'])
plt.suptitle('Regional Background Stations 4MDA8', fontsize = 16)

traffic_4mda8.plot(subplots = True,ylim = (50,180),marker = 'o', layout = (2,3), title = ['QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Traffic Stations 4MDA8', fontsize = 16)
#%% SOMO35
beijing_over35 = beijing_mda8[beijing_mda8.iloc[:,:]>=35]
over35_by_year = [group[1] for group in beijing_over35.groupby(beijing_over35.index.year)]
beijing_SOMO35 = []
for row in over35_by_year:
    rows = pd.DataFrame(row.sum())
    beijing_SOMO35.append(rows)
test = pd.concat(beijing_SOMO35)
beijing_SOMO35_byyear = pd.read_csv('/home/lp555/Beijing/Observations/Sinaapp/data/SOMO35_all_stat.csv', index_col = ['Year'])
beijing_SOMO35_byyear.columns.values
beijing_SOMO35_byyear.plot(subplots = True, marker = 'o', layout = (5,7), title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY',
       'FTHY', 'YG', 'GC', 'FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG',
       'PG', 'HR', 'MY', 'YQ', 'DL', 'BDL', 'MYSK', 'DGC', 'YLD', 'YD',
       'LLH', 'QM', 'YDMN', 'XZMB', 'NSH', 'DSH'], legend = False)
plt.suptitle('SOMO35 stations')
#%% number of exceedances of MDA8 - not to think about this shit for now
mda8_by_year = [group[1] for group in beijing_mda8.groupby(beijing_mda8.index.year)]
for row in mda8_by_year:
    no_over_50 = pd.DataFrame(row)[pd.DataFrame(row) > 50].count()
    print(no_over_50)
#%% mda8 ym
beijing_mda8_ym = beijing_mda8.resample('Y').mean()
urban_mda8_ym = beijing_mda8_ym.loc['2015-12-31 00:00:00':, 'DS':'GC']
suburban_mda8_ym = beijing_mda8_ym.loc['2015-12-31 00:00:00':, 'FS':'YQ']
dl_mda8_ym = pd.DataFrame(beijing_mda8_ym.loc['2015-12-31 00:00:00':, 'DL'])
regional_bg_mda8_ym = beijing_mda8_ym.loc['2015-12-31 00:00:00':,'BDL':'LLH' ]
traffic_mda8_ym = beijing_mda8_ym.loc['2015-12-31 00:00:00':, 'QM':'DSH']
#%%
urban_mda8_ym.plot(subplots = True, ylim = (30, 60), layout = (4,3), marker = 'o', legend = False, title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY','FTHY', 'YG', 'GC']) #, title = 'Urban Stations Daily Mean')
plt.suptitle('Urban Stations Yearly Mean MDA8', fontsize = 16)
#%%
suburban_mda8_ym.plot(subplots = True, ylim = (45, 65), marker = 'o', layout = (4,3),title = ['FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ'])
plt.suptitle('Suburban Stations Yearly Mean MDA8', fontsize = 16)

dl_mda8_ym.plot(marker = 'o', ylim = (40, 60))
plt.suptitle('DingLing Yearly Mean MDA8', fontsize = 16)

regional_bg_mda8_ym.plot(subplots = True, ylim = (30, 70), marker = 'o', layout = (2,3), title = ['BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH'])
plt.suptitle('Regional Background Stations Yearly Mean MDA8', fontsize = 16)

traffic_mda8_ym.plot(subplots = True, ylim = (25, 50), marker = 'o', layout = (2,3), title = ['QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Traffic Stations Yearly Mean MDA8', fontsize = 16)
#%% SOMO35
#%% import NO2 data for comparison
path = r'/home/lp555/Beijing/Observations/Sinaapp/data/Beijing_NO2_2014_to_2019'
NO2_files = glob.glob(os.path.join(path, "*.csv"))
df_NO2 = pd.concat((pd.read_csv(f) for f in NO2_files))
df_NO2.columns = ['Date','pollutant', 'DS','TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ','ZWY', 'FTHY', 'YG', 'GC', 'FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ', 'DL', 'BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH', 'QM', 'YDMN', 'XZMB', 'NSH', 'DSH']
df_NO2.Date = pd.to_datetime(df_NO2.Date, dayfirst = True)
df_NO2.sort_values(by = ['Date'], inplace = True)
beijing_NO2 = df_NO2.set_index('Date')
wl_NO2 = pd.DataFrame(beijing_NO2.WL/1.88)
#%%
wl_NO2_dm = wl_NO2.resample('D').mean()
wl_NO2_dm.plot()
#%%
wl_NO2_mmdm = wl_NO2_dm.resample('M').mean()
wl_NO2_mmdm.plot()
#%%
mk_result_NO2 = mk.seasonal_test(wl_NO2_mmdm, period = 12)
print(mk_result_NO2)
#%%
wl_O3_mmoy = wl_O3_mmdm.groupby(wl_O3_mmdm.index.month).mean()
wl_O3_mmoy.plot()
#%% O3 average Diurnal profile
wl_O3_dpoy = wl_O3.groupby(wl_O3.index.hour).mean()
wl_O3_dpoy.plot()
#%%  NO2 average diurnal profile
wl_NO2_dpoy = wl_NO2.groupby(wl_NO2.index.hour).mean()
wl_NO2_dpoy.plot()
#%% Traffic monitor sites
dsh_O3 = pd.DataFrame(beijing_O3.DSH.astype(float)/2)
dsh_O3_dm = dsh_O3.resample('D').mean()
#%%
dsh_O3_mmdm = dsh_O3_dm.resample('M').mean()
dsh_O3_mmdm.plot()
#%%
dsh_O3_mmoy = dsh_O3_mmdm.groupby(dsh_O3_mmdm.index.month).mean()
dsh_O3_mmoy.plot()
#%%
dsh_O3_dpoy = dsh_O3.groupby(dsh_O3.index.hour).mean()
dsh_O3_dpoy.plot()
#%% Try to do a seasonal analysis - try this later but do it manually for now
mlist = [[12, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
slist = ['Winter', 'Spring', 'Summer', 'Autumn']
sdict = {k: v for v, ks in zip(slist, mlist) for k in ks}

#wl_season = wl_O3.groupby(wl_O3.index.month.map(sdict.get))
#wl_season.groups
#%%
wl_seasons = []
for group in wl_O3.groupby(wl_O3.index.month.map(sdict.get)):
    wl_seasons.append(group[1])
print(wl_seasons)
    
#%% pdf of different stations -wl
avg_8hr_wl = (wl_O3.rolling(8, min_periods = 6).mean())
avg_8hr_wl = pd.DataFrame(avg_8hr_wl)
mda8_wl = avg_8hr_wl.resample('D').max()
mda8_wl.plot.kde()
#%% pdf dsh
avg_8hr_dsh = (dsh_O3.rolling(8, min_periods = 6).mean())
avg_8hr_dsh = pd.DataFrame(avg_8hr_dsh)
mda8_dsh = avg_8hr_dsh.resample('D').max()
mda8_dsh.plot.kde()
#%% plot together
def pdf_bj(df_station):
    df_station = pd.DataFrame(df_station/2)
    #df_station = pd.to_datetime(df_station.Date, dayfirst = True)
    df_avg_8hr_station = pd.DataFrame(df_station.rolling(8, min_periods = 6).mean())
    df_mda8_station = df_avg_8hr_station.resample('D').max()
    return df_mda8_station.plot.kde(), df_mda8_station.hist()

pdf_bj(beijing_O3.DS)
    