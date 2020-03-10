#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 11:41:33 2020

@author: lp555
"""

#%%
import pandas as pd
import pymannkendall as mk
import numpy as np
#%%
av_all = pd.read_csv('/home/lp555/Delhi/Observations/AnandVihar_O3_NO_NO2_2015_2019.csv')
av_all.columns = ['Date', 'NO2', 'NO', 'O3']
av_all.Date = pd.to_datetime(av_all.Date, dayfirst = True)
av_all = av_all.set_index('Date')
av_all.replace(to_replace = ["None"], value = np.nan, inplace = True)
#%% Ozone
av_O3 = pd.DataFrame(av_all.O3.astype(float)/2)
av_O3_dm = av_O3.resample('D').mean()
av_O3_dm.plot()
#%%
av_O3_mmdm = av_O3_dm.resample('M').mean()
av_O3_mmdm.plot(marker = 'o')
#%%
av_O3_dpoy = av_O3.groupby(av_O3.index.hour).mean()
av_O3_dpoy.plot()