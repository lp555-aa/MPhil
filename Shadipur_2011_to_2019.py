#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 11:10:19 2020

@author: lp555
"""

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymannkendall as mk
#%%
Shadipur_Del = pd.read_csv('/home/lp555/Delhi/Observations/Delhi_Shadipur_Hourly_2011_to_2019_edited.csv')
del Shadipur_Del['To Date']
#%%
Shadipur_Del.columns = ['date','O3']
Shadipur_Del.date = pd.to_datetime(Shadipur_Del.date, dayfirst = True)
Shadipur_Del.set_index('date', inplace = True)
#%%
Shadipur_Del.replace(to_replace=["None"], value=np.nan, inplace=True)
Shadipur_Del['O3'] = Shadipur_Del['O3'].astype(float)
#%% MDA 8
avg_8hr_O3 = (Shadipur_Del['O3'].rolling(8,min_periods = 6).mean())
avg_8hr_O3 = pd.DataFrame(avg_8hr_O3)
times_dl = avg_8hr_O3.index.values - pd.Timedelta('8h')
avg_8hr_O3.index.values[:] = times_dl
mda8 = avg_8hr_O3.resample('D').max()/2
ax = mda8.plot(figsize=(9,3), color='k')
ax.set_ylabel('MDA8 O$_3$ Delhi (ppb)')
plt.show()
#%% Monthly average of MDA8 O3
monthly_mda8mean = mda8.O3.resample('M').mean()
monthly_mda8mean.drop(monthly_mda8mean.index[0])
ax = monthly_mda8mean.plot(figsize=(9,3), color = 'k', marker = 'o')
ax.set_ylabel('monthly mean Delhi')
#%% daily mean
daily_mean = Shadipur_Del.O3[32:].resample('D').mean()
monthly_mean = Shadipur_Del.O3[32:].resample('M').mean()
#%% insert the daily mean values from CPCB
daily_mean_new = pd.read_csv('/home/lp555/Delhi/Observations/Delhi_Shadipur_daily_2011_to_2019_edited.csv', usecols = [0,1])
daily_mean_new.date = pd.to_datetime(daily_mean_new.date, dayfirst = True)
daily_mean_new.set_index('date', inplace = True)
daily_mean_new.replace(0, np.nan, inplace=True)
monthly_mean_of_dm = daily_mean_new.resample('M').mean()
#%%
ax = monthly_mean_of_dm[36:].plot(figsize=(9,3), color = 'k', marker = 'o')
ax.set_ylabel('monthly mean of daily mean Shadipur Delhi 2014 to 2019')
#%% SMK
mk.seasonal_test(monthly_mean_of_dm[36:], period = 12)
#%%
monthly_mean_of_dm["O3"]
mmdm = np.array(monthly_mean_of_dm["O3"])
mmdm = mmdm[:96]
#%%
mmdm_reshape = np.reshape(mmdm, (8,12))
mmdm_month_mean = np.nanmean(mmdm_reshape, axis = 0)
plt.plot(mmdm_month_mean)
#%%
mmdm_month_std = np.nanstd(mmdm_reshape, axis = 0)
plt.errorbar(np.arange(1,13, 1), mmdm_month_mean, yerr = mmdm_month_std)
#%% crearing a linear fit of the monthly mean data - first step converting pandas dataframe to a numpy array
#from scipy import stats
#mmdm1 = np.array(monthly_mean_of_dm["O3"])
#x = monthly_mean_of_dm.index
#x = np.array(monthly_mean_of_dm.index)
#x = np.arange(0,107,1)
#res = stats.theilslopes(mmdm1, x, 0.90)
l#sq_res = stats.linregress(x, mmdm1)
#%% when do a linear regression, check for missing data first with the following line 
monthly_mean_of_dm.isnull.values.any()
#%% plot a histogram to see if the data follows a normal distribution - here roughly
monthly_mean_of_dm.hist()
#%% to get rid of some outliers following the 68-95-99.7 rule - here get rid of outliers that are out of bound of 3 stds
std_dev = 3
mmdm2 = monthly_mean_of_dm[(np.abs(stats.zscore(monthly_mean_of_dm.O3)) < float(std_dev)).all(axis=1)]
mmdm2.plot(figsize=(18,5))
#%%
import seaborn
