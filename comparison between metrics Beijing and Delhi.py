#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 12:20:25 2019

@author: lp555
"""

#%% 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import datetime
#%% import data from Beijing - taking Wanliu
beijing_2016 = pd.read_csv('/home/lp555/Beijing/Observations/Sinaapp/data/WL_obs_2016.csv')
beijing_2016['date'] = pd.to_datetime(beijing_2016['date'], dayfirst = True)
beijing_2016.set_index('date', inplace = True)
#%% MDA8
#%%
#convert to 8 hours rolling 
avg_8hr_O3_bj = (beijing_2016['o3'].rolling(8, min_periods = 6).mean())
avg_8hr_O3_bj = pd.DataFrame(avg_8hr_O3_bj)
#%% cut off the final 8 hours - not useful in this circumstance as nan
times_bj = avg_8hr_O3_bj.index.values - pd.Timedelta('8h')
avg_8hr_O3_bj.index.values[:] = times_bj
#%% make the plot
mda8_bj = avg_8hr_O3_bj.resample('D').max()/2 #gives mixing ratio in ppb
ax = mda8_bj.loc['2016'].plot(figsize=(9,3), color='k')
ax.set_ylabel('MDA8 O$_3$ Beijing (ppb)')
plt.show()
#%% import data from Delhi - taking DTU
delhi_2019 = pd.read_csv('file:///home/lp555/Delhi/Observations/Delhi_DTU_Hourly_2019_edited.csv')#, skiprows = 18, header = None)
del delhi_2019['To Date']
#%%
delhi_2019.columns = ['date','O3']
delhi_2019['date'] = pd.to_datetime(delhi_2019['date'], dayfirst = True)
delhi_2019.set_index('date', inplace = True)
#%% replace None (object) to np.nan in order to convert strings to floats
delhi_2019.replace(to_replace=["None"], value=np.nan, inplace=True)
delhi_2019['O3'] = delhi_2019['O3'].astype(float)
#%% MDA8 Delhi
avg_8hr_O3_dl = (delhi_2019['O3'].rolling(8,min_periods = 6).mean())
avg_8hr_O3_dl = pd.DataFrame(avg_8hr_O3_dl)
times_dl = avg_8hr_O3_dl.index.values - pd.Timedelta('8h')
avg_8hr_O3_dl.index.values[:] = times_dl
#%% make the plot
mda8_dl = avg_8hr_O3_dl.resample('D').max()/2
ax = mda8_dl.loc['2019'].plot(figsize=(9,3), color='k')
ax.set_ylabel('MDA8 O$_3$ Delhi (ppb)')
plt.show()
#%% not sure about the definition of 4MDA8 - so ask! - three different methods
#%% no minute data so impossible for the calculation of MDA1 - may just get the maximum daily value
mda1_bj = beijing_2016['o3'].resample('D').max()/2
mda1_bj = pd.DataFrame(mda1_bj)
mda1_dl = delhi_2019['O3'].resample('D').max()/2
mda1_dl = pd.DataFrame(mda1_dl)
ax = mda1_bj.loc['2016'].plot(figsize=(9,3), color='k')
ax.set_ylabel('MDA1 O$_3$ Beijing (ppb)')
plt.show()
ax = mda1_dl.loc['2019'].plot(figsize=(9,3), color='k')
ax.set_ylabel('MDA1 O$_3$ Delhi (ppb)')
plt.show()
#%% SOMO35
somo35_bj = mda8_bj[mda8_bj['o3'] >= 35]
somo35_dl = mda8_dl[mda8_dl['O3'] >= 35]
somo35bj = somo35_bj['o3'].sum() #14240.410714285714 ppb 365 days
somo35dl = somo35_dl['O3'].sum() #10646.359047619033 ppb ~340 days
#%% SOMO10
somo10_bj = mda8_bj[mda8_bj['o3'] >= 10]
somo10_dl = mda8_dl[mda8_dl['O3'] >= 10]
somo10bj = somo10_bj['o3'].sum() #16836.401785714286 ppb 365 days
somo10dl = somo10_dl['O3'].sum() #13638.174077380927 ppb ~340 days
#%% the 4th highest W90 5-h cumulative exposure index - wtf?
#%% plain time series for both cities
fig, ax = plt.subplots(figsize=(18,10))
ax.plot(beijing_2016.index,
        beijing_2016['o3']/2,
        color = 'b')
ax.set(xlabel = 'date',
       ylabel = 'O$_3$ / ppbv',
       title = 'Beijing 2016')
plt.gca()
plt.show()
fig, ax = plt.subplots(figsize=(18,10))
ax.plot(delhi_2019.index,
        delhi_2019['O3']/2,
        color = 'b')
ax.set(xlabel = 'date',
       ylabel = 'O$_3$ / ppbv',
       title = 'Delhi 2019')
plt.gca()
plt.show()
#%% annual percentiles (median, 5th, 25th, 75th and 95th)
#Beijing
beijing_2016.o3.mean()/2 # mean = 27.155310741228597
beijing_2016.o3.median()/2 # median = 20.0
beijing_2016.o3.quantile(0.05)/2 # 5th quantile = 1.0
beijing_2016.o3.quantile(0.25)/2 # 25th quantile = 2.5
beijing_2016.o3.quantile(0.75)/2 # 75th quantile = 41.0
beijing_2016.o3.quantile(0.95)/2 # 95 quantile = 87.0
beijing_2016.o3.max()/2 # max value 159.0
#%%
#Delhi
delhi_2019.mean()/2 # mean = 23.510335
delhi_2019.median()/2 # median = 17.825
delhi_2019.quantile(0.05)/2 # 5th quantile = 3.125
delhi_2019.quantile(0.25)/2 # 25th quantile = 8.24
delhi_2019.quantile(0.75)/2 # 75th quantile = 35.325
delhi_2019.quantile(0.95)/2 # 95th quantile = 62.305
delhi_2019.max()/2 # max value 99.215
#%% for the seasonal percentiles, need to figure out the ozone seasons - 
beijing_2016.o3[4000:6000].max()/2 #using intervals after finding the ozone seasons based on time series
#%% Annual and summertime mean of MDA8
mda8_bj.mean() #46.724079
mda8_dl.mean() #41.648386
#%% the number of exceedances of daily maximum 8-h values greater than 50, 60, 70 and 80 ppb per year
#Beijing
mda8_bj[mda8_bj > 50].count() # 132 days
mda8_bj[mda8_bj > 60].count() # 107 days
mda8_bj[mda8_bj > 70].count() # 89 days
mda8_bj[mda8_bj > 80].count() # 61 days
#%%
#Delhi
mda8_dl[mda8_dl > 50].count() # 84 days
mda8_dl[mda8_dl > 60].count() # 47 days
mda8_dl[mda8_dl > 70].count() # 13 days
mda8_dl[mda8_dl > 80].count() # 4 days
#%% the number of exceedances of daily maximum 1-h values greater than 90, 100, 120 ppb
#Beijing
mda1_bj[mda1_bj > 90].count() # 72 days
mda1_bj[mda1_bj > 100].count() # 51 days
mda1_bj[mda1_bj > 120].count() # 23 days
#%%
#Delhi
mda1_dl[mda1_dl > 90].count() # 17 days
mda1_dl[mda1_dl > 100].count() # 0 days
mda1_dl[mda1_dl > 120].count() # 0 days
#%%  The running mean of the three-month average of the daily 1-h maximum
#Beijing
rm_bj = (mda1_bj['o3'].rolling(90).mean())
#%%
#Delhi
rm_dl = (mda1_dl['O3'].rolling(90).mean())
#%% monthly mean
#Beijing
monthly_mean_bj = beijing_2016.o3.resample('M').mean()/2
ax = monthly_mean_bj.loc['2016'].plot(figsize=(9,3), color='k', marker = 'o')
ax.set_ylabel('monthly mean Beijing')
#%%
#Delhi
monthly_mean_dl = delhi_2019.O3.resample('M').mean()/2
monthly_mean_dl.drop(monthly_mean_dl.index[0])
ax = monthly_mean_dl.loc['2019'].plot(figsize=(9,3), color = 'k', marker = 'o')
ax.set_ylabel('monthly mean Delhi')
#%% monthly mean of daily mean
#daily_mean_beijing = beijing_2016['o3'].resample('D').mean()/2
#daily_mean_beijing = pd.DataFrame(daily_mean_beijing)
#monthly_mean_bj_2 = daily_mean_beijing.o3.resample('M').mean()
#%% Daytime average - 
DT_bj = beijing_2016.between_time(datetime.time(8), datetime.time(20),include_start = True, include_end = False)
DTAvg_bj = DT_bj.o3.resample('M').mean()
ax = DTAvg_bj.loc['2016'].plot(figsize=(9,3), color='k', marker = 'o')
ax.set_ylabel('monthly mean Beijing (DT)')
#%%
DT_dl = delhi_2019.between_time(datetime.time(8), datetime.time(20),include_start = True, include_end = False)
DTAvg_dl = DT_dl.O3.resample('M').mean()
DTAvg_dl = pd.DataFrame(DTAvg_dl)
DTAvg_dl.drop(DTAvg_dl.index[0])
ax = DTAvg_dl.loc['2019'].plot(figsize = (9,3), color ='k', marker = 'o')
ax.set_ylabel('monthly mean Delhi (DT)')
#%%
e90bj = 72
e100bj = 51
e120bj = 23
e_bj = np.array([e90bj, e100bj, e120bj])
m_e_bj = np.array([90, 100, 120])
fig,ax = plt.subplots(figsize=(9,5))
ax.plot(m_e_bj,
         e_bj,
         'ro')
ax.set(xlabel = 'MDA1 over x ppb',
       ylabel = 'number of days',
       title = 'Beijing')
plt.show()
#%%
e90dl = 17
e100dl = 0
e120dl = 0
e_dl = np.array([e90dl, e100dl, e120dl])
m_e_dl = np.array([90, 100, 120])
fig,ax = plt.subplots(figsize=(9,5))
ax.plot(m_e_dl,
         e_dl,
         'ro')
ax.set(xlabel = 'MDA1 over x ppb',
       ylabel = 'number of days',
       title = 'Delhi')
plt.show()
#%%
e50bj = 132
e60bj = 107
e70bj = 89
e80bj = 61
e_bj1 = np.array([e50bj, e60bj, e70bj, e80bj])
m_e_bj1 = np.array([50,60,70,80])
fig,ax = plt.subplots(figsize=(9,5))
ax.plot(m_e_bj1,
         e_bj1,
         'ro')
ax.set(xlabel = 'MDA8 over x ppb',
       ylabel = 'number of days',
       title = 'Beijing')
plt.show()
#%%
e50dl = 84
e60dl = 47
e70dl = 13
e80dl = 4
e_dl1 = np.array([e50dl, e60dl, e70dl, e80dl])
m_e_dl1 = np.array([50,60,70,80])
fig,ax = plt.subplots(figsize=(9,5))
ax.plot(m_e_dl1,
         e_dl1,
         'ro')
ax.set(xlabel = 'MDA8 over x ppb',
       ylabel = 'number of days',
       title = 'Delhi')
plt.show()
#%%
mda8_bj.o3.nlargest(4)
#%%
mda8_dl.O3.nlargest(4)