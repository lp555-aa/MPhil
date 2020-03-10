#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:31:02 2020

@author: lp555
"""

#%% HUMAN HEALTH METRICS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os 
import glob
import datetime as dt
#%%
path = r'/home/lp555/Beijing/Observations/Sinaapp/data/Beijing_O3_2014_to_2019'
O3_files = glob.glob(os.path.join(path, "*.csv"))
df_O3 = pd.concat(pd.read_csv(f) for f in O3_files)
df_O3.columns = ['Date','pollutant', 'DS','TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ','ZWY', 'FTHY', 'YG', 'GC', 'FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ', 'DL', 'BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH', 'QM', 'YDMN', 'XZMB', 'NSH', 'DSH']
df_O3.Date = pd.to_datetime(df_O3.Date, dayfirst = True)
df_O3.sort_values(by=['Date'], inplace = True)
beijing_O3 = df_O3.set_index('Date')
del beijing_O3['pollutant']
beijing_O3 = beijing_O3/2
#%% mda8
mda8_O3 = pd.DataFrame((beijing_O3.rolling(8, min_periods = 6).mean()).resample('D').max())
#for column in mda8_O3:
 #   plt.xlabel("time", fontsize = 16)
  #  plt.ylabel("mixing ratio / ppb", fontsize = 16)
   # plt.title("MDA8 over years")
    #plt.show(mda8_O3[column])
mda8_O3.plot()
#%% wanliu as example
wl_O3 = pd.DataFrame(mda8_O3.WL)
plt.xlabel("time", fontsize = 16)
plt.ylabel("mixing ratio / ppb", fontsize = 16)
plt.title("MDA8 2014 to 2019", fontsize = 18)
plt.plot(wl_O3)
plt.show()
#%% 4MDA8 wanliu as example
#byyear = []
#for group in wl_O3.groupby(wl_O3.index.year):
    #byyear.append(group)
wl_by_year = [group[1] for group in wl_O3.groupby(wl_O3.index.year)]
#%%
mda8_4_all = []
fourth_mda8_wl = []
for df in wl_by_year:
    values = df.nlargest(4, ['WL'])
    mda8_4_all.append(values)
for df in mda8_4_all:
    value = df.nsmallest(1, ['WL'])
    fourth_mda8_wl.append(value)
print(fourth_mda8_wl)
#%%
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
fmda8(mda8_O3.DS)
#%%
fmda8_all = pd.DataFrame()
for column in mda8_O3:
    #fmda8_all.append(fmda8(mda8_O3[column]))
    fmda8_all = pd.concat((station for station in fmda8(mda8_O3[column])))
        
    