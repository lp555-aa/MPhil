#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 23:27:45 2020

@author: lp555
"""

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#%%
SH_O3 = pd.read_csv('/home/lp555/Delhi/Observations/CPCB/Delhi_Shadipur_Hourly_2011_to_2019_edited.csv')
del SH_O3['From Date']
#%%
SH_O3.columns = ['Date','O3']
SH_O3.set_index('Date', inplace = True)
SH_O3.index = pd.to_datetime(SH_O3.index, dayfirst = True)
SH_O3.replace(to_replace=["None"], value=np.nan, inplace=True)
SH_O3['O3'] = SH_O3['O3'].astype(float)
SH_O3 = SH_O3/2
print(SH_O3)
