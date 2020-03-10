#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 10:45:27 2019

@author: lp555
"""

#%%
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import netCDF4 as nc
import datetime as dt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
#%matplotlib inline
#%% import summer ozone dataframe
summer_data = pd.read_csv('/home/lp555/Delhi/Observations/BHAM_IIT_summer_ozone_final_edited.csv', parse_dates=['date (IST)'], infer_datetime_format=True, index_col=['date (IST)'])
summer_data.index =  pd.to_datetime(summer_data.index, dayfirst = True)
summer_ozone = pd.DataFrame(summer_data, columns = ['O3 (ppb)'])
#%% plot
# Create the plot space upon which to plot the data
fig, ax = plt.subplots(figsize=(18, 10))

# Add the x-axis and the y-axis to the plot
ax.plot(summer_data.index,
        summer_ozone, '-',
        color='purple')

#to look at the data with logrithmic scale
#ax.semilogy(summer_data.index,
        #ozone_data, '-',
        #color='purple')

# Set title and labels for axes
ax.set(xlabel="Date and time",
       ylabel="Ozone / ppb",
       title="Summer Ozone levels")

# Clean up the x axis dates
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
ax.xaxis.set_major_formatter(DateFormatter("%d/%m"))

axes = plt.gca()
axes.set_ylim([0,160])

plt.show()
#%% autumn ozone
autumn_data = pd.read_csv('/home/lp555/Delhi/Observations/BHAM_IIT_autumn_ozone_final_edited.csv', index_col = ['date'])
autumn_data.index = pd.to_datetime(autumn_data.index, dayfirst = True)
autumn_ozone = pd.DataFrame(autumn_data, columns = ['O3'])
#%% make the plot
fig, ax = plt.subplots(figsize=(18, 10))

ax.plot(autumn_data.index,
        autumn_ozone, '-',
        color='purple')

# Set title and labels for axes
ax.set(xlabel="Date and time",
       ylabel="Ozone / ppb",
       title="Autumn Ozone levels")

# Clean up the x axis dates
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
ax.xaxis.set_major_formatter(DateFormatter("%d/%m"))

axes = plt.gca()
axes.set_ylim([0,135])

plt.show()
#%% winter ozone
winter_data = pd.read_csv('/home/lp555/Delhi/Observations/BHAM_IIT_winter_ozone_final_edited.csv', index_col = ['date (IST)'])
winter_data.index = pd.to_datetime(winter_data.index, dayfirst = True)
winter_ozone = pd.DataFrame(winter_data, columns = ['O3 (ppb)'])
#%% make the plot
fig, ax = plt.subplots(figsize=(18, 10))

ax.plot(winter_data.index,
        winter_ozone, '-',
        color='purple')

# Set title and labels for axes
ax.set(xlabel="Date and time",
       ylabel="Ozone / ppb",
       title="winter Ozone levels")

# Clean up the x axis dates
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
ax.xaxis.set_major_formatter(DateFormatter("%d/%m"))

axes = plt.gca()
axes.set_ylim([0,120])

plt.show()
#%% Beijing Summer 
data_201705 = pd.read_csv('/home/lp555/Beijing/Observations/APHH/O3, CO, NO, NO2, NOy, SO2/york-gas-api_iap-beijing_20170517_v3.na', sep = '\s+', skiprows = 50, header = None)
data_201705.columns = ('time', 'O3', 'O3 flag', 'CO', 'CO flag', 'NO', 'NO flag', 'NO2', 'NO2 flag', 'NOy', 'NOy flag', 'SO2', 'SO2 flag' )
time_201705 = pd.DataFrame(data_201705, columns = ['time'])
time_201705['c_time'] = pd.TimedeltaIndex(time_201705['time'], unit='d')+dt.datetime(2017,1,1)
converted_time = pd.DataFrame(time_201705, columns = ['c_time'])
data_201705['time'] = converted_time
#%% minute data time series
data_201705_1 = data_201705.apply(lambda x:np.where(x>9999, np.nan, x) if x.name != 'time' else x)
#%%
summer_ozone[30698:]
#data_201705_1.set_index('time', inplace = True)
#%%
fig, ax = plt.subplots(figsize = (18,10))
ax.plot(data_201705_1['time'][0:26839],
        data_201705_1['O3'][0:26839], 
        color = 'r')
ax.plot(data_201705_1['time'][0:26879],
        summer_ozone[30698:], 
        color='green')
ax.set(xlabel='date',
       ylabel='O$_3$ / ppb',
       title = 'APHH 201705')
plt.gca()
plt.show()