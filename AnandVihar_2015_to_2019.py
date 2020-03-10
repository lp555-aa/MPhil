#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 10:31:07 2020

@author: lp555
"""

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymannkendall as mk
import statsmodels.api as sm
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
#%% read data - deal with missing data and convert data type to float
Anand_Del = pd.read_csv('/home/lp555/Delhi/Observations/AnandVihar_hourly_2015_2019_edited.csv')
Anand_Del.columns = ['date', 'O3']
Anand_Del.date = pd.to_datetime(Anand_Del.date, dayfirst = True)
Anand_Del.set_index('date', inplace = True)
Anand_Del.replace(to_replace = ["None"], value = np.nan, inplace = True)
Anand_Del.O3 = Anand_Del.O3.astype(float)/2
#%% resample to daily mean - MDA 8 may not be useful
daily_mean = Anand_Del.O3.resample('D').mean()
daily_mean = pd.DataFrame(daily_mean)
#%% resample to monthly mean of daily mean
mmdm = daily_mean.O3.resample('M').mean()
ax = mmdm.plot(figsize=(9,3), color = 'k', marker = 'o')
ax.set_ylabel('monthly mean of daily mean Anand Delhi 2015 to 2019')
#%% Seasonal Mann Kendall (SMK) test on the trend (ozone season)
mk.seasonal_test(mmdm, period = 4)
#%%