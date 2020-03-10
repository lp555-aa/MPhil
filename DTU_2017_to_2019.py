#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 13:46:51 2020

@author: lp555
"""

#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#%% O3 and NO2
dtu_2019 = pd.read_csv('/home/lp555/Delhi/Observations/DTU_Hourly_2019_O3_NO2.csv')
dtu_2019.Date = pd.to_datetime(dtu_2019.Date, dayfirst = True)
dtu_2019.set_index('Date', inplace = True)
#%%
dtu_2019.replace(to_replace=["None"], value=np.nan, inplace=True)
dtu_2019.NO2 = dtu_2019.NO2.astype(float)/1.88
dtu_2019.Ozone = dtu_2019.Ozone.astype(float)/2
dtu_2019.plot()
#%% O3 and NO and NO2
dtu_2019_1 = pd.read_csv('/home/lp555/Delhi/Observations/DTU_Hourly_2019_O3_NO_NO2.csv')
dtu_2019_1.Date = pd.to_datetime(dtu_2019_1.Date, dayfirst = True)
dtu_2019_1.set_index('Date', inplace = True)

#%%
dtu_2019_1.replace(to_replace=["None"], value=np.nan, inplace=True)
dtu_2019_1.NO2 = dtu_2019_1.NO2.astype(float)/1.88
dtu_2019_1.O3 = dtu_2019_1.O3.astype(float)/2
dtu_2019_1.NO = dtu_2019_1.O3.astype(float)/1.25
dtu_2019_1.plot()
#%%
dtu_2019_NO2 = dtu_2019_1.NO2
dtu_2019_NO2.plot()
#%% 2018
dtu_2018 = pd.read_csv('/home/lp555/Delhi/Observations/DTU_Hourly_2018_O3_NO_NO2.csv')
dtu_2018.Date = pd.to_datetime(dtu_2018.Date, dayfirst = True)
dtu_2018.set_index('Date', inplace = True)
dtu_2018.replace(to_replace=["None"], value=np.nan, inplace=True)
dtu_2018.NO2 = dtu_2018.NO2.astype(float)/1.88
dtu_2018.O3 = dtu_2018.O3.astype(float)/2
dtu_2018.NO = dtu_2018.NO.astype(float)/1.25
#dtu_2018.plot()
dtu_2018.NO2.plot()
#%%
dtu_2017 = pd.read_csv('/home/lp555/Delhi/Observations/DTU_Hourly_2017_NO_NO2.csv')
dtu_2017.Date = pd.to_datetime(dtu_2017.Date, dayfirst = True)
dtu_2017.replace(to_replace=["None"], value=np.nan,inplace = True)
dtu_2017.set_index('Date', inplace = True)
dtu_2017.NO2 = dtu_2017.NO2.astype(float)/1.88
dtu_2017.NO2.plot()
#%% would like to make a yearly averaged diurnal profile - show in one day
