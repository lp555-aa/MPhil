#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 15:06:47 2020

@author: lp555
"""

#%%
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pymannkendall as mk
import seaborn as sns
#%%
path = '/home/lp555/Delhi/Observations/CPCB/csv'
delhi_files = glob.glob(os.path.join(path, "*.csv"))
df_O3 = []
df_NO2 = []
df_NO = []
for df in delhi_files:
    df_all = pd.read_csv(df, index_col = ['Date'])
    df_O3.append(pd.DataFrame(df_all.iloc[:,0]))
for df in delhi_files:
    df_all = pd.read_csv(df, index_col = ['Date'])
    df_NO2.append(pd.DataFrame(df_all.iloc[:,1]))   
for df in delhi_files:
    df_all = pd.read_csv(df, index_col = ['Date'])
    df_NO.append(pd.DataFrame(df_all.iloc[:,2]))
#%%
delhi_O3 = pd.concat(df_O3, axis = 1, sort = True)
delhi_O3.index = pd.to_datetime(delhi_O3.index, dayfirst = True)
delhi_O3.replace(to_replace=["None"], value=np.nan, inplace=True)
delhi_O3 = delhi_O3.astype(float)/2
delhi_O3.columns = ['AL','AV','AK','AN','BA','BC','EA','SH','SF']
delhi_O3 = delhi_O3.sort_index()
#%%
delhi_NO2 = pd.concat(df_NO2, axis = 1, sort = True)
delhi_NO2.index = pd.to_datetime(delhi_NO2.index, dayfirst = True)
delhi_NO2.replace(to_replace=["None"], value=np.nan, inplace=True)
delhi_NO2['NO2'] = delhi_NO2['NO2'].astype(float)
delhi_NO2.columns = ['AL','AV','AK','AN','BA','BC','EA','SH','SF']
delhi_NO2 = delhi_NO2.sort_index()
#%%
delhi_NO = pd.concat(df_NO, axis = 1, sort = True)
delhi_NO.index = pd.to_datetime(delhi_NO.index, dayfirst = True)
delhi_NO.replace(to_replace=["None"], value=np.nan, inplace=True)
delhi_NO['NO'] = delhi_NO['NO'].astype(float)
delhi_NO.columns = ['AL','AV','AK','AN','BA','BC','EA','SH','SF']
delhi_NO = delhi_NO.sort_index()
#%%
delhi_O3_mmoy = delhi_O3.groupby(delhi_O3.index.month).mean()
delhi_O3_mmoy.plot(subplots = True, ylim = (0, 45), layout = (3,3), title =['AL','AV','AK','AN','BA','BC','EA','SH','SF'], legend = False, marker = 'o')
plt.xlabel('Month')
plt.ylabel('Ozone Mixing Ratio / ppb')
plt.suptitle('Monthly Mean over 2018 - 2019', fontsize = 16)
#%%
delhi_O3_dp = delhi_O3.groupby(delhi_O3.index.hour).mean()
delhi_O3_dp.plot(subplots = True, layout = (3,3), legend = False, title = ['AL','AV','AK','AN','BA','BC','EA','SH','SF'])
plt.xlabel('Time')
plt.ylabel('Ozone Mixing Ratio / ppb')
plt.suptitle('Diurnal Cycle over 2018 - 2019', fontsize = 16)
#%%
delhi_mda8 = (delhi_O3.rolling(8, min_periods = 6).mean()).resample('D').max()
delhi_mda8.plot(subplots = True, legend = False, layout = (3,3), title = ['AL','AV','AK','AN','BA','BC','EA','SH','SF'])
plt.suptitle('MDA 8 2018 - 2019')
#%%
delhi_mda1 = delhi_O3.resample('D').max()
delhi_mda1.plot(subplots = True, legend = False, layout = (3,3), title = ['AL','AV','AK','AN','BA','BC','EA','SH','SF'])
plt.suptitle('MDA 1 2018 - 2019')
#%% 4mda8
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
for column in delhi_mda8:
    all_stat = fmda8(delhi_mda8[column])

    for row in all_stat:
        rows = pd.DataFrame(row)
        all_stats.append(rows)
delhi_fmda8_test = pd.concat(all_stats, ignore_index = True, sort = False)
#%% daily mean
delhi_dm = delhi_O3.resample('D').mean()
delhi_dm.plot(subplots = True, layout = (3,3), legend = False, title = ['AL','AV','AK','AN','BA','BC','EA','SH','SF'])
plt.suptitle('Daily Mean 2018 - 2019')
#%% monthly mean of daily mean
delhi_mmdm = delhi_dm.resample('M').mean()
delhi_mmdm.plot(subplots = True, layout = (3,3), marker = 'o', legend = False, title = ['AL','AV','AK','AN','BA','BC','EA','SH','SF'])
plt.suptitle('Monthly Mean of Daily Mean', fontsize = 16)
#%% pdf to see station types
def pdf_dl_mda8(df_station):
    df_avg_8hr_station = pd.DataFrame(df_station.rolling(8, min_periods = 6).mean())
    df_mda8_station = df_avg_8hr_station.resample('D').max()
    plt.title('MDA8 Ozone All Stations', fontsize = 18)
    plt.xlabel('Ozone mixing ratio / ppb', fontsize = 16)
    plt.ylabel('Normalised frequency', fontsize = 16 )
    return  sns.distplot(df_mda8_station.dropna(), kde = True, hist = True, hist_kws = dict(edgecolor='k', linewidth = 1))
for column in delhi_O3:
    pdf_dl_mda8(delhi_O3[column])
    plt.legend(pd.DataFrame(delhi_O3[column]).columns.values)
plt.show()
#%%
m_list = [[12,1,2], [3, 4, 5], [6, 7, 8, 9], [10, 11]]
s_list = ['Winter', 'Pre-monsoon', 'Summer monsoon', 'Post-monsoon']
s_dict = {k: v for v, ks in zip(s_list, m_list) for k in ks}
#%% get the seasons!
delhi_seasons = []
for group in delhi_O3.groupby(delhi_O3.index.month.map(s_dict.get)):
    delhi_seasons.append(group[1])
print(delhi_seasons)
#%%
delhi_winter = delhi_seasons[0]
delhi_prem = delhi_seasons[1]
delhi_sm = delhi_seasons[2]
delhi_postm = delhi_seasons[3]
#%%
delhi_winter_dp = delhi_winter.groupby(delhi_winter.index.hour).mean()
delhi_prem_dp = delhi_prem.groupby(delhi_prem.index.hour).mean()
delhi_sm_dp = delhi_sm.groupby(delhi_sm.index.hour).mean()
delhi_postm_dp = delhi_postm.groupby(delhi_postm.index.hour).mean()
#%%
delhi_winter_dp.plot(subplots = True, marker = 'o', layout = (3,3), legend = False, title = ['AL','AV','AK','AN','BA','BC','EA','SH','SF'])
plt.suptitle('Winter Diurnal Cycle', fontsize = 16)
#%%
delhi_prem_dp.plot(subplots = True, marker = 'o', layout = (3,3), legend = False, title = ['AL','AV','AK','AN','BA','BC','EA','SH','SF'])
plt.suptitle('Pre-monsoon Diurnal Cycle', fontsize = 16)
#%%
delhi_sm_dp.plot(subplots = True, marker = 'o', layout = (3,3), legend = False, title = ['AL','AV','AK','AN','BA','BC','EA','SH','SF'])
plt.suptitle('Summer Monsoon Diurnal Cycle', fontsize = 16)
#%%
delhi_postm_dp.plot(subplots = True, marker = 'o', layout = (3,3), legend = False, title = ['AL','AV','AK','AN','BA','BC','EA','SH','SF'])
plt.suptitle('Post-monsoon Diurnal Cycle', fontsize = 16)
#%%
delhi_winter_dp.iloc[:,1]
#%%
VA_seasonal_dp_list = [pd.DataFrame(delhi_winter_dp.iloc[:,1]), pd.DataFrame(delhi_prem_dp.iloc[:,1]), pd.DataFrame(delhi_sm_dp.iloc[:,1]), pd.DataFrame(delhi_postm_dp.iloc[:,1])]
VA_seasonal_dp = pd.concat(VA_seasonal_dp_list, axis = 1)
VA_seasonal_dp.columns = ['Winter','Pre-monsoon','Summer monsoon','Post-monsoon']
VA_seasonal_dp.plot(title = 'Diurnal Cycles of different seasons - VA')
plt.legend(VA_seasonal_dp.columns.values)
#%%
