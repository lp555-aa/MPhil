#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:56:52 2020

@author: lp555
"""

#%% O3 vs. CO vs. NO2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
#%%
path = r'/home/lp555/Beijing/Observations/Sinaapp/data/Beijing_O3_2014_to_2019'
O3_files = glob.glob(os.path.join(path, "*.csv"))
df_O3 = pd.concat((pd.read_csv(f) for f in O3_files))
df_O3.columns = ['Date','pollutant', 'DS','TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ','ZWY', 'FTHY', 'YG', 'GC', 'FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ', 'DL', 'BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH', 'QM', 'YDMN', 'XZMB', 'NSH', 'DSH']
df_O3.Date = pd.to_datetime(df_O3.Date, dayfirst = True)
df_O3.sort_values(by=['Date'], inplace = True)
beijing_O3 = df_O3.set_index('Date')
del beijing_O3['pollutant']
beijing_O3 = beijing_O3/2
#%%
path = r'/home/lp555/Beijing/Observations/Sinaapp/data/Beijing_CO_2014_to_2019'
CO_files = glob.glob(os.path.join(path, "*csv"))
df_CO = pd.concat((pd.read_csv(f) for f in CO_files))
df_CO.columns = ['Date','pollutant', 'DS','TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ','ZWY', 'FTHY', 'YG', 'GC', 'FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ', 'DL', 'BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH', 'QM', 'YDMN', 'XZMB', 'NSH', 'DSH']
df_CO.Date = pd.to_datetime(df_CO.Date, dayfirst = True)
df_CO.sort_values(by=['Date'], inplace = True)
beijing_CO = df_CO.set_index('Date')
del beijing_CO['pollutant']
beijing_CO = beijing_CO/1.1642
#%% can define a function for the same work but will do later
path = r'/home/lp555/Beijing/Observations/Sinaapp/data/Beijing_NO2_2014_to_2019'
NO2_files = glob.glob(os.path.join(path, "*csv"))
df_NO2 = pd.concat((pd.read_csv(f) for f in NO2_files))
df_NO2.columns = ['Date','pollutant', 'DS','TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ','ZWY', 'FTHY', 'YG', 'GC', 'FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ', 'DL', 'BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH', 'QM', 'YDMN', 'XZMB', 'NSH', 'DSH']
df_NO2.Date = pd.to_datetime(df_NO2.Date, dayfirst = True)
df_NO2.sort_values(by=['Date'], inplace = True)
beijing_NO2 = df_NO2.set_index('Date')
del beijing_NO2['pollutant']
beijing_NO2 = beijing_NO2/1.88
#%% define a function for diurnal profile
def dp_pollutants(df_pollutants):
    df_dp_pollutants = df_pollutants.groupby(df_pollutants.index.hour).mean()
    return (df_dp_pollutants)
dp_O3 = dp_pollutants(beijing_O3)
dp_NO2 = dp_pollutants(beijing_NO2)
dp_CO = dp_pollutants(beijing_CO)
#%%
dp_WL_O3 = pd.DataFrame(dp_O3.WL)
dp_WL_CO = pd.DataFrame(dp_CO.WL)
dp_WL_NO2 = pd.DataFrame(dp_NO2.WL)
wl_list = [dp_WL_O3, dp_WL_CO, dp_WL_NO2]   
#for d in wl_list[1:]:
#    d.columns = wl_list[0].columns
WL_pollutants = pd.concat(wl_list, axis = 1)
WL_pollutants.columns = ["O3", "CO", "NO2"]
WL_pollutants.plot()
#%%
beijing_O3_ym = beijing_O3.resample('Y').mean()
beijing_CO_ym = beijing_CO.resample('Y').mean()
beijing_NO2_ym = beijing_NO2.resample('Y').mean()
beijing_O3_ym.WL.plot(title = 'Wanliu Ozone Yearly Mean', marker = 'o', ylim = (10, 40))
plt.ylabel('Ozone Mixing Ratio / ppb')
plt.xlabel('Year')
#%%
plt.figure()
beijing_CO_ym.WL.plot(title = 'Wanliu Carbon Monoxide Yearly Mean', marker = 'o', ylim = (0,2))
plt.ylabel('Carbon Monoxide Mixing Ratio / ppm')
plt.xlabel('Year')
#%%
plt.figure()
beijing_NO2_ym.WL.plot(title = 'Wanliu Nitrogen Dioxide Yearly Mean', marker = 'o', ylim = (10, 50))
plt.ylabel('Nitrogen Dioxide Mixing Ratio / ppb')
plt.xlabel('Year')
#%% forget about CO for now
m_list = [[12,1,2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
s_list = ['Winter', 'Spring', 'Summer', 'Autumn']
s_dict = {k: v for v, ks in zip(s_list, m_list) for k in ks}
beijing_O3_seasons = []
for group in beijing_O3.groupby(beijing_O3.index.month.map(s_dict)):
    beijing_O3_seasons.append(group[1])
print(beijing_O3_seasons)
#%%
beijing_O3_dp_seasons = []
for l in beijing_O3_seasons:
    beijing_O3_dp_seasons.append(dp_pollutants(l))
beijing_autumn_O3_dp = beijing_O3_dp_seasons[0]
beijing_spring_O3_dp = beijing_O3_dp_seasons[1]
beijing_summer_O3_dp = beijing_O3_dp_seasons[2]
beijing_winter_O3_dp = beijing_O3_dp_seasons[3]
#%%
m_list = [[12,1,2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
s_list = ['Winter', 'Spring', 'Summer', 'Autumn']
s_dict = {k: v for v, ks in zip(s_list, m_list) for k in ks}
beijing_NO2_seasons = []
for group in beijing_NO2.groupby(beijing_NO2.index.month.map(s_dict)):
    beijing_NO2_seasons.append(group[1])
print(beijing_NO2_seasons)
#%%
beijing_NO2_dp_seasons = []
for l in beijing_NO2_seasons:
    beijing_NO2_dp_seasons.append(dp_pollutants(l))
beijing_autumn_NO2_dp = beijing_NO2_dp_seasons[0]
beijing_spring_NO2_dp = beijing_NO2_dp_seasons[1]
beijing_summer_NO2_dp = beijing_NO2_dp_seasons[2]
beijing_winter_NO2_dp = beijing_NO2_dp_seasons[3]
#%% for better legend quality
from matplotlib.lines import Line2D
#%%
beijing_autumn_comp = pd.concat([beijing_autumn_O3_dp, beijing_autumn_NO2_dp], axis = 0)
def dp_comp_stations(df):
    df_O3 = df[0:24]
    df_NO2 = df[24:]
    ax = df_O3.plot()
    df_NO2.plot(ax = ax)
    colors = ['blue', 'orange']
    #lines = [Line2D([0], [0], color=c, linewidth=3, linestyle='--') for c in colors]
    labels = ['O3', 'NO2']
    plt.legend(labels)
    plt.title(df.columns.values[0], fontsize = 16)
    plt.xlabel('hour', fontsize = 12)
    plt.ylabel('O3 and NO2 mixing ratio / ppb', fontsize = 12)
    return plt.show()

for column in beijing_autumn_comp:
    dp_comp_stations(pd.DataFrame(beijing_autumn_comp[column]))
#%%
beijing_spring_comp = pd.concat([beijing_spring_O3_dp, beijing_spring_NO2_dp], axis = 0)
for column in beijing_spring_comp:
    dp_comp_stations(pd.DataFrame(beijing_spring_comp[column]))
#%%
urban_bj_O3 = beijing_O3.loc[:, 'DS':'GC']
suburban_bj_O3 = beijing_O3.loc[:, 'FS':'YQ']
dl_bj_O3 = pd.DataFrame(beijing_O3.loc[:, 'DL'])
regional_bg_bj_O3 = beijing_O3.loc[:, 'BDL':'LLH']
traffic_bj_O3 = beijing_O3.loc[:, 'QM':'DSH']
urban_bj_NO2 = beijing_NO2.loc[:, 'DS':'GC']
suburban_bj_NO2 = beijing_NO2.loc[:, 'FS':'YQ']
dl_bj_NO2 = pd.DataFrame(beijing_NO2.loc[:, 'DL'])
regional_bg_bj_NO2 = beijing_NO2.loc[:, 'BDL':'LLH']
traffic_bj_NO2 = beijing_NO2.loc[:, 'QM':'DSH']
#%%
def yearly_mean(df):
    return df.groupby(df.index.year).mean()
urban_bj_O3_ym = yearly_mean(urban_bj_O3)
urban_bj_NO2_ym = yearly_mean(urban_bj_NO2)
#%%
for column1, column2 in urban_bj_O3_ym, urban_bj_NO2_ym:
    ax = pd.DataFrame(urban_bj_O3_ym[column1]).plot()
    pd.DataFrame(urban_bj_NO2_ym[column2]).plot(ax = ax)
    plt.show()