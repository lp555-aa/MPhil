#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:31:27 2020

@author: lp555
"""

#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os
#%% import multiple csv files and concatenate them into one single dataframe - take notes!  
path = r'/home/lp555/Beijing/Observations/Sinaapp/data/Beijing_O3_2014_to_2019'
O3_files = glob.glob(os.path.join(path, "*.csv"))
df_O3 = pd.concat((pd.read_csv(f) for f in O3_files))
df_O3.columns = ['Date','pollutant', 'DS','TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ','ZWY', 'FTHY', 'YG', 'GC', 'FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ', 'DL', 'BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH', 'QM', 'YDMN', 'XZMB', 'NSH', 'DSH']
#%% 
df_O3.Date = pd.to_datetime(df_O3.Date, dayfirst = True)
df_O3.sort_values(by=['Date'], inplace = True)
beijing_O3 = df_O3.set_index('Date')
del beijing_O3['pollutant']
beijing_O3 = beijing_O3/2
#%%
wl_O3 = beijing_O3.WL
wl_avg8 = pd.DataFrame(wl_O3.rolling(8, min_periods = 6).mean())
wl_mda8 = wl_avg8.resample('D').max()
#wl_mda8.hist(edgecolor = 'black', bins = 30)
plt.title('MDA8 Ozone Wanliu', fontsize=18)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.ylabel('Normalised frequency', fontsize = 16)
ax = sns.distplot(wl_mda8.dropna(), kde = True, hist = True, hist_kws = dict(edgecolor='black', linewidth = 1))
#%% stupid attempt of iteration but worth think about
#df_mda8_all = pd.DataFrame()
#data_list=[]
#for df_station in beijing_O3:
    #df_mda8 = pd.DataFrame(beijing_O3[df_station].rolling(8, min_periods = 6).mean()).resample('D').max()
    #data_list.append(df_mda8)
#%%
df_mda8_all = pd.DataFrame(beijing_O3.rolling(8, min_periods = 6).mean()).resample('D').max()
df_mda8_all.plot.kde()
#%% try with mda8
def pdf_bj_mda8(df_station):
    df_avg_8hr_station = pd.DataFrame(df_station.rolling(8, min_periods = 6).mean())
    df_mda8_station = df_avg_8hr_station.resample('D').max()
    plt.title('MDA8 Ozone All Stations', fontsize = 18)
    plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
    plt.ylabel('Normalised frequency', fontsize = 16 )
    return  sns.distplot(df_mda8_station.dropna(), kde = True, hist = True, hist_kws = dict(edgecolor='k', linewidth = 1))
for column in beijing_O3:
    pdf_bj_mda8(beijing_O3[column])
plt.show()
#%% try with hourly data
def pdf_bj(df_station):
    plt.title('Hourly Ozone', fontsize = 18)
    plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
    plt.ylabel('Normalised frequency', fontsize = 16 )
    return sns.distplot(df_station.dropna(), kde = True, hist = True, hist_kws = dict(edgecolor='k', linewidth = 1))
for column in beijing_O3:
    pdf_bj(beijing_O3[column])
plt.show()    
#%% export the different station types
urban_bj = beijing_O3.loc[:, 'DS':'GC']
suburban_bj = beijing_O3.loc[:, 'FS':'YQ']
dl_bj = pd.DataFrame(beijing_O3.loc[:, 'DL'])
regional_bg_bj = beijing_O3.loc[:, 'BDL':'LLH']
traffic_bj = beijing_O3.loc[:, 'QM':'DSH']
cat_dict = {"urban_sites":urban_bj, 
            "suburban_sites":suburban_bj, 
            "dingling_bg": dl_bj, 
            "regional_bg_sites": regional_bg_bj, 
            "traffic_monitoring_sites": traffic_bj}
#for k, v in cat_dict.items(): # when iterating through a dictionary remember to use  '.items()' !!
    #v.to_csv('/home/lp555/Beijing/Observations/Sinaapp/data/stations_by_type/{}.csv'.format(k))
#%%
urban_bj_mda8 = df_mda8_all.loc[:, 'DS':'GC']
suburban_bj_mda8 = df_mda8_all.loc[:, 'FS':'YQ']
dl_bj_mda8 = pd.DataFrame(df_mda8_all.loc[:, 'DL'])
regional_bg_bj_mda8 = df_mda8_all.loc[:, 'BDL':'LLH']
traffic_bj_mda8 = df_mda8_all.loc[:, 'QM':'DSH']
cat_dict = {"urban_sites_mda8":urban_bj_mda8, 
            "suburban_sites_mda8":suburban_bj_mda8, 
            "dingling_bg_mda8": dl_bj_mda8, 
            "regional_bg_sites_mda8": regional_bg_bj_mda8, 
            "traffic_monitoring_sites_mda8": traffic_bj_mda8}
#for k, v in cat_dict.items(): # when iterating through a dictionary remember to use  '.items()' !!
    #v.to_csv('/home/lp555/Beijing/Observations/Sinaapp/data/stations_by_type/{}.csv'.format(k))
#%%
plt.figure()
for column in urban_bj_mda8:
    pdf_bj(urban_bj_mda8[column])
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Urban sites', fontsize = 18)
#%%
plt.figure()
for column in suburban_bj_mda8:
    pdf_bj(suburban_bj_mda8[column])
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Suburban sites', fontsize = 18)
#%%
plt.figure()
for column in traffic_bj_mda8:
    pdf_bj(traffic_bj_mda8[column])
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Traffic sites', fontsize = 18)
#%%
plt.figure()
for column in regional_bg_bj_mda8:
    pdf_bj(regional_bg_bj_mda8[column])
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Regional background sites', fontsize = 18)
#%%
plt.figure()
for column in dl_bj_mda8:
    pdf_bj(dl_bj_mda8[column])
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Ding Ling', fontsize = 18)
#%%
mlist = [[12, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
slist = ['Winter', 'Spring', 'Summer', 'Autumn']
sdict = {k: v for v, ks in zip(slist, mlist) for k in ks}
urban_seasons = []
for group in urban_bj_mda8.groupby(urban_bj_mda8.index.month.map(sdict.get)):
    urban_seasons.append(group[1])
print(urban_seasons)
#%%
urban_autumn = urban_seasons[0]
urban_spring = urban_seasons[1]
urban_summer = urban_seasons[2]
urban_winter = urban_seasons[3]
#%%
pd.DataFrame(urban_autumn.WL).columns
#%%
plt.figure()
for column in urban_autumn:
    pdf_bj(urban_autumn[column])
plt.legend(urban_autumn.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Urban sites autumn', fontsize = 18)
#%%
plt.figure()
for column in urban_spring:
    pdf_bj(urban_spring[column])
plt.legend(urban_spring.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Urban sites spring', fontsize = 18)
#%%
plt.figure()
for column in urban_summer:
    pdf_bj(urban_summer[column])
plt.legend(urban_summer.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Urban sites summer', fontsize = 18)
#%%
plt.figure()
for column in urban_winter:
    pdf_bj(urban_winter[column])
plt.legend(urban_winter.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Urban sites winter', fontsize = 18)
#%% def a function to do the work for me!
mlist = [[12, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
slist = ['Winter', 'Spring', 'Summer', 'Autumn']
sdict = {k: v for v, ks in zip(slist, mlist) for k in ks}
suburban_seasons = []
for group in suburban_bj_mda8.groupby(suburban_bj_mda8.index.month.map(sdict.get)):
    suburban_seasons.append(group[1])
print(suburban_seasons)
#%%
suburban_autumn = suburban_seasons[0]
suburban_spring = suburban_seasons[1]
suburban_summer = suburban_seasons[2]
suburban_winter = suburban_seasons[3]
#%%
plt.figure()
for column in suburban_autumn:
    pdf_bj(suburban_autumn[column])
plt.legend(suburban_autumn.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Suburban sites autumn', fontsize = 18)
#%%
plt.figure()
for column in suburban_spring:
    pdf_bj(suburban_spring[column])
plt.legend(suburban_spring.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Suburban sites spring', fontsize = 18)
#%%
plt.figure()
for column in suburban_summer:
    pdf_bj(suburban_summer[column])
plt.legend(suburban_summer.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Suburban sites summer', fontsize = 18)
#%%
plt.figure()
for column in suburban_winter:
    pdf_bj(suburban_winter[column])
plt.legend(suburban_winter.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Suburban sites winter', fontsize = 18)
#%%
mlist = [[12, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
slist = ['Winter', 'Spring', 'Summer', 'Autumn']
sdict = {k: v for v, ks in zip(slist, mlist) for k in ks}
traffic_seasons = []
for group in traffic_bj_mda8.groupby(traffic_bj_mda8.index.month.map(sdict.get)):
    traffic_seasons.append(group[1])
print(traffic_seasons)
#%%
traffic_autumn = traffic_seasons[0]
traffic_spring = traffic_seasons[1]
traffic_summer = traffic_seasons[2]
traffic_winter = traffic_seasons[3]
#%%
plt.figure()
for column in traffic_autumn:
    pdf_bj(traffic_autumn[column])
plt.legend(traffic_autumn.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Traffic sites autumn', fontsize = 18)
#%%
plt.figure()
for column in traffic_spring:
    pdf_bj(traffic_spring[column])
plt.legend(traffic_spring.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Traffic sites spring', fontsize = 18)
#%%
plt.figure()
for column in traffic_summer:
    pdf_bj(traffic_summer[column])
plt.legend(traffic_summer.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Traffic sites summer', fontsize = 18)
#%%
plt.figure()
for column in traffic_winter:
    pdf_bj(traffic_winter[column])
plt.legend(traffic_winter.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Traffic sites winter', fontsize = 18)
#%%
mlist = [[12, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
slist = ['Winter', 'Spring', 'Summer', 'Autumn']
sdict = {k: v for v, ks in zip(slist, mlist) for k in ks}
regional_seasons = []
for group in regional_bg_bj_mda8.groupby(regional_bg_bj_mda8.index.month.map(sdict.get)):
    regional_seasons.append(group[1])
print(regional_seasons)
#%%
regional_autumn = regional_seasons[0]
regional_spring = regional_seasons[1]
regional_summer = regional_seasons[2]
regional_winter = regional_seasons[3]
#%%
plt.figure()
for column in regional_autumn:
    pdf_bj(regional_autumn[column])
plt.legend(regional_autumn.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Regional Background sites autumn', fontsize = 18)
#%%
plt.figure()
for column in regional_spring:
    pdf_bj(regional_spring[column])
plt.legend(regional_spring.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Regional Background sites spring', fontsize = 18)
#%%
plt.figure()
for column in regional_summer:
    pdf_bj(regional_summer[column])
plt.legend(regional_summer.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Regional Background sites summer', fontsize = 18)
#%%
plt.figure()
for column in regional_winter:
    pdf_bj(regional_winter[column])
plt.legend(regional_winter.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Regional Background sites winter', fontsize = 18)
#%%
mlist = [[12, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
slist = ['Winter', 'Spring', 'Summer', 'Autumn']
sdict = {k: v for v, ks in zip(slist, mlist) for k in ks}
dl_seasons = []
for group in dl_bj_mda8.groupby(dl_bj_mda8.index.month.map(sdict.get)):
    dl_seasons.append(group[1])
print(dl_seasons)
#%%
dl_autumn = dl_seasons[0]
dl_spring = dl_seasons[1]
dl_summer = dl_seasons[2]
dl_winter = dl_seasons[3]
#%%
plt.figure()
for column in dl_autumn:
    pdf_bj(dl_autumn[column])
plt.legend(dl_autumn.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Ding Ling autumn', fontsize = 18)
#%%
plt.figure()
for column in dl_spring:
    pdf_bj(dl_spring[column])
plt.legend(dl_spring.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Ding Ling spring', fontsize = 18)
#%%
plt.figure()
for column in dl_summer:
    pdf_bj(dl_summer[column])
plt.legend(dl_summer.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Ding Ling summer', fontsize = 18)
#%%
plt.figure()
for column in dl_winter:
    pdf_bj(dl_winter[column])
plt.legend(dl_winter.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Ding Ling winter', fontsize = 18)
#%%
mlist = [[12, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
slist = ['Winter', 'Spring', 'Summer', 'Autumn']
sdict = {k: v for v, ks in zip(slist, mlist) for k in ks}
beijing_seasons = []
for group in df_mda8_all.groupby(df_mda8_all.index.month.map(sdict.get)):
    beijing_seasons.append(group[1])
print(beijing_seasons)
#%%
beijing_autumn = beijing_seasons[0]
beijing_spring = beijing_seasons[1]
beijing_summer = beijing_seasons[2]
beijing_winter = beijing_seasons[3]
#%%
plt.figure()
for column in beijing_autumn:
    pdf_bj(beijing_autumn[column])
plt.legend(beijing_autumn.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Beijing autumn', fontsize = 18)
#%%
plt.figure()
for column in beijing_spring:
    pdf_bj(beijing_spring[column])
plt.legend(beijing_spring.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Beijing spring', fontsize = 18)
#%%
plt.figure()
for column in beijing_summer:
    pdf_bj(beijing_summer[column])
plt.legend(beijing_summer.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Beijing summer', fontsize = 18)
#%%
plt.figure()
for column in beijing_winter:
    pdf_bj(beijing_winter[column])
plt.legend(beijing_winter.columns.values)
plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
plt.title('Beijing winter', fontsize = 18)