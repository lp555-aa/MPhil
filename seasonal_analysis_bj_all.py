#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:30:32 2020

@author: lp555
"""

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymannkendall as mk
import glob
import os
import statsmodels.api as sm
#%%
path = r'/home/lp555/Beijing/Observations/Sinaapp/data/Beijing_O3_2014_to_2019'
O3_files = glob.glob(os.path.join(path, "*.csv"))
df_O3 = pd.concat((pd.read_csv(f) for f in O3_files))
df_O3.columns = ['Date','pollutant', 'DS','TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ','ZWY', 'FTHY', 'YG', 'GC', 'FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ', 'DL', 'BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH', 'QM', 'YDMN', 'XZMB', 'NSH', 'DSH']
df_O3.Date = pd.to_datetime(df_O3.Date, dayfirst = True)
df_O3.sort_values(by=['Date'], inplace = True)
beijing_O3 = df_O3.set_index('Date')
del beijing_O3['pollutant']
beijing_O3 = beijing_O3/2 # to convert ug/m3 to ppb
#%%
beijing_mmoy = beijing_O3.groupby(beijing_O3.index.month).mean()
ax = beijing_mmoy.plot(subplots = True, legend = False, marker = 'o', layout = (5,7), title = ['DS','TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ','ZWY', 'FTHY', 'YG', 'GC', 'FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ', 'DL', 'BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH', 'QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Monthly Mean Over 6 Years All Stations')
#ax[4,6].set_xticklabels(beijing_mmoy.index.values)
#%%
mlist = [[12, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]
slist = ['Winter', 'Spring', 'Summer', 'Autumn']
sdict = {k: v for v, ks in zip(slist, mlist) for k in ks}
beijing_seasons = []
for group in beijing_O3.groupby(beijing_O3.index.month.map(sdict.get)):
    beijing_seasons.append(group[1])
print(beijing_seasons)
#%%
beijing_season_dp = []
for row in beijing_seasons:
    seasonal_dp = row.groupby(row.index.hour).mean()
    beijing_season_dp.append(seasonal_dp)
print(beijing_season_dp)
#%% Autumn
beijing_autumn_dp = beijing_season_dp[0]
beijing_spring_dp = beijing_season_dp[1]
beijing_summer_dp = beijing_season_dp[2]
beijing_winter_dp = beijing_season_dp[3]
urban_autumn_dp = beijing_autumn_dp.loc[:, 'DS':'GC']
suburban_autumn_dp = beijing_autumn_dp.loc[:, 'FS':'YQ']
dl_autumn_dp = pd.DataFrame(beijing_autumn_dp.loc[:, 'DL'])
regional_bg_autumn_dp = beijing_autumn_dp.loc[:,'BDL':'LLH' ]
traffic_autumn_dp = beijing_autumn_dp.loc[:, 'QM':'DSH']
#%%
wl_season_comparison_list = [pd.DataFrame(beijing_autumn_dp.WL),pd.DataFrame(beijing_spring_dp.WL),pd.DataFrame(beijing_summer_dp.WL),pd.DataFrame(beijing_winter_dp.WL)]
wl_season_comparison = pd.concat(wl_season_comparison_list, axis = 1)
wl_season_comparison.columns  = ['autumn', 'spring', 'summer', 'winter']
wl_season_comparison.plot(legend = True, marker = 'o')
plt.xlabel('Time')
plt.ylabel('Ozone Mixing Ratio / ppb')
plt.title('Wanliu seasonal diurnal cycle', fontsize  = 16)
plt.show()
#%%
ds_season_comparison_list = [pd.DataFrame(beijing_autumn_dp.DS),pd.DataFrame(beijing_spring_dp.DS),pd.DataFrame(beijing_summer_dp.DS),pd.DataFrame(beijing_winter_dp.DS)]
ds_season_comparison = pd.concat(ds_season_comparison_list, axis = 1)
ds_season_comparison.columns  = ['autumn', 'spring', 'summer', 'winter']
ds_season_comparison.plot(legend = True, marker = 'o')
plt.xlabel('Time')
plt.ylabel('Ozone Mixing Ratio / ppb')
plt.title('Dongsi seasonal diurnal cycle', fontsize  = 16)
plt.show()
#%%
all_stations_seasons_list = [beijing_autumn_dp, beijing_spring_dp, beijing_summer_dp, beijing_winter_dp]
all_stations_seasons = pd.concat(all_stations_seasons_list)
all_stations_seasons = all_stations_seasons.reindex(sorted(all_stations_seasons.columns), axis = 1)
#%%
wanliu_season_comparison_list = [pd.DataFrame(all_stations_seasons.WL[0:24]), pd.DataFrame(all_stations_seasons.WL[24:48]), pd.DataFrame(all_stations_seasons.WL[48:72]), pd.DataFrame(all_stations_seasons.WL[72:96])]
wanliu_season_comparison = pd.concat(wanliu_season_comparison_list, axis = 1)
wanliu_season_comparison.columns = ['autumn', 'spring', 'summer', 'winter']
wanliu_season_comparison.plot(legend = True, marker = 'o')
column_name = (pd.DataFrame(all_stations_seasons.WL).columns.values)
plt.xlabel('Time')
plt.ylabel('Ozone Mixing Ratio / ppb')
plt.title('{column_name[0]} seasonal diurnal profiles'.format(column_name = column_name))
#%% according to wanliu but not mean time of sunrise
(wanliu_season_comparison.iloc[16, 0] - wanliu_season_comparison.iloc[7,0])/(16-7)
(wanliu_season_comparison.iloc[17, 2] - wanliu_season_comparison.iloc[7,2])/(17-7)
def net_prod_r_season(df):
    autumn = (df.iloc[16, 0] - df.iloc[7, 0])/(16 - 7)
    spring = (df.iloc[17, 1] - df.iloc[7, 1])/(17 - 7)
    summer = (df.iloc[16, 2] - df.iloc[7, 2])/(16 - 7)
    winter = (df.iloc[15, 3] - df.iloc[8, 3])/(15 - 8)
    return {'Autumn_rate': autumn, 'Spring_rate': spring, 'Summer_rate': summer, 'Winter_rate': winter}
print(net_prod_r_season(wanliu_season_comparison))
#%%
def station_seasonal_dp(df):
    df_season_comparison_list = [pd.DataFrame(df[0:24]), pd.DataFrame(df[24:48]), pd.DataFrame(df[48:72]), pd.DataFrame(df[72:96])]
    df_season_comparison = pd.concat(df_season_comparison_list, axis = 1)
    df_season_comparison.columns = ['autumn', 'spring', 'summer', 'winter']
    
    df_season_comparison.plot(legend = True, marker = 'o')
    column_name = (pd.DataFrame(df).columns.values)
    def net_prod_r_season(df_season_comparison):
        autumn = (df_season_comparison.iloc[16, 0] - df_season_comparison.iloc[7, 0])/(16 - 7)
        spring = (df_season_comparison.iloc[17, 1] - df_season_comparison.iloc[7, 1])/(17 - 7)
        summer = (df_season_comparison.iloc[16, 2] - df_season_comparison.iloc[7, 2])/(16 - 7)
        winter = (df_season_comparison.iloc[15, 3] - df_season_comparison.iloc[8, 3])/(15 - 8)
        return {'Autumn_rate': autumn, 'Spring_rate': spring, 'Summer_rate': summer, 'Winter_rate': winter}
    plt.xlabel('Time')
    plt.ylabel('Ozone Mixing Ratio / ppb')
    plt.title('{column_name[0]} seasonal diurnal profiles'.format(column_name = column_name))
    #plt.title('df seasonal diurnal cycle', fontsize = 16)
    plt.figtext(.17, .855, net_prod_r_season(df_season_comparison))
    return plt.show(), net_prod_r_season(df_season_comparison)
station_seasonal_dp(all_stations_seasons.TT)
#%%
for column in all_stations_seasons:
    station_seasonal_dp(all_stations_seasons[column])
#%%
urban_autumn_dp.plot(subplots = True, ylim = (0,50), layout = (4,3), marker = 'o', legend = False, title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY','FTHY', 'YG', 'GC']) #, title = 'Urban Stations Daily Mean')
plt.suptitle('Urban Stations Autumn Diurnal Profile', fontsize = 16)

suburban_autumn_dp.plot(subplots = True, ylim = (0,50), marker = 'o', layout = (4,3),title = ['FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ'])
plt.suptitle('Suburban Stations Autumn Diurnal Profile', fontsize = 16)

dl_autumn_dp.plot(marker = 'o', ylim = (0,50))
plt.suptitle('DingLing Autumn Diurnal Profile', fontsize = 16)

regional_bg_autumn_dp.plot(subplots = True, ylim = (0,50), marker = 'o', layout = (2,3), title = ['BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH'])
plt.suptitle('Regional Background Stations Autumn Diurnal Profile', fontsize = 16)

traffic_autumn_dp.plot(subplots = True, ylim = (0,50), marker = 'o', layout = (2,3), title = ['QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Traffic Stations Autumn Diurnal Profile', fontsize = 16)

plt.show()
#%% Spring
urban_spring_dp = beijing_spring_dp.loc[:, 'DS':'GC']
suburban_spring_dp = beijing_spring_dp.loc[:, 'FS':'YQ']
dl_spring_dp = pd.DataFrame(beijing_spring_dp.loc[:, 'DL'])
regional_bg_spring_dp = beijing_spring_dp.loc[:,'BDL':'LLH' ]
traffic_spring_dp = beijing_spring_dp.loc[:, 'QM':'DSH']
#%%
urban_spring_dp.plot(subplots = True, ylim = (0,80), layout = (4,3), marker = 'o', legend = False, title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY','FTHY', 'YG', 'GC']) #, title = 'Urban Stations Daily Mean')
plt.suptitle('Urban Stations Spring Diurnal Profile', fontsize = 16)

suburban_spring_dp.plot(subplots = True, ylim = (0,80), marker = 'o', layout = (4,3),title = ['FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ'])
plt.suptitle('Suburban Stations Spring Diurnal Profile', fontsize = 16)

dl_spring_dp.plot(marker = 'o', ylim = (0,80))
plt.suptitle('DingLing Spring Diurnal Profile', fontsize = 16)

regional_bg_spring_dp.plot(subplots = True, ylim = (0,80), marker = 'o', layout = (2,3), title = ['BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH'])
plt.suptitle('Regional Background Stations Spring Diurnal Profile', fontsize = 16)

traffic_spring_dp.plot(subplots = True, ylim = (0,80), marker = 'o', layout = (2,3), title = ['QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Traffic Stations Spring Diurnal Profile', fontsize = 16)
#%%
urban_winter_dp = beijing_winter_dp.loc[:, 'DS':'GC']
suburban_winter_dp = beijing_winter_dp.loc[:, 'FS':'YQ']
dl_winter_dp = pd.DataFrame(beijing_winter_dp.loc[:, 'DL'])
regional_bg_winter_dp = beijing_winter_dp.loc[:,'BDL':'LLH' ]
traffic_winter_dp = beijing_winter_dp.loc[:, 'QM':'DSH']
#%%
urban_winter_dp.plot(subplots = True, ylim = (0,40), layout = (4,3), marker = 'o', legend = False, title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY','FTHY', 'YG', 'GC']) #, title = 'Urban Stations Daily Mean')
plt.suptitle('Urban Stations Winter Diurnal Profile', fontsize = 16)

suburban_winter_dp.plot(subplots = True, ylim = (0,40), marker = 'o', layout = (4,3),title = ['FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ'])
plt.suptitle('Suburban Stations Winter Diurnal Profile', fontsize = 16)

dl_winter_dp.plot(marker = 'o', ylim = (0,40))
plt.suptitle('DingLing Winter Diurnal Profile', fontsize = 16)

regional_bg_winter_dp.plot(subplots = True, ylim = (0,40), marker = 'o', layout = (2,3), title = ['BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH'])
plt.suptitle('Regional Background Stations Winter Diurnal Profile', fontsize = 16)

traffic_winter_dp.plot(subplots = True, ylim = (0,40), marker = 'o', layout = (2,3), title = ['QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Traffic Stations Winter Diurnal Profile', fontsize = 16)
#%%
urban_summer_dp = beijing_summer_dp.loc[:, 'DS':'GC']
suburban_summer_dp = beijing_summer_dp.loc[:, 'FS':'YQ']
dl_summer_dp = pd.DataFrame(beijing_summer_dp.loc[:, 'DL'])
regional_bg_summer_dp = beijing_summer_dp.loc[:,'BDL':'LLH' ]
traffic_summer_dp = beijing_summer_dp.loc[:, 'QM':'DSH']
#%%
beijing_season_trend = []
for row in beijing_seasons:
    seasonal_trend = row.groupby(row.index.year).mean()
    beijing_season_trend.append(seasonal_trend)
#print(beijing_season_trend)
beijing_autumn_trend = beijing_season_trend[0]
beijing_spring_trend = beijing_season_trend[1]
beijing_summer_trend = beijing_season_trend[2]
beijing_winter_trend = beijing_season_trend[3]
#%%
urban_autumn_trend = beijing_autumn_trend.loc[:, 'DS':'GC']
suburban_autumn_trend = beijing_autumn_trend.loc[:, 'FS':'YQ']
dl_autumn_trend = pd.DataFrame(beijing_autumn_trend.loc[:, 'DL'])
regional_bg_autumn_trend = beijing_autumn_trend.loc[:,'BDL':'LLH' ]
traffic_autumn_trend = beijing_autumn_trend.loc[:, 'QM':'DSH']
#%%
urban_autumn_trend.plot(subplots = True, ylim = (0,40), layout = (4,3), marker = 'o', legend = False, title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY','FTHY', 'YG', 'GC']) #, title = 'Urban Stations Daily Mean')
plt.suptitle('Urban Stations Autumn Trend', fontsize = 16)

suburban_autumn_trend.plot(subplots = True, ylim = (0,40), marker = 'o', legend = False, layout = (4,3),title = ['FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ'])
plt.suptitle('Suburban Stations Autumn Trend', fontsize = 16)

dl_autumn_trend.plot(marker = 'o', ylim = (0,40), legend = False)
plt.suptitle('DingLing Autumn Trend', fontsize = 16)

regional_bg_autumn_trend.plot(subplots = True, ylim = (0,40), legend = False, marker = 'o', layout = (2,3), title = ['BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH'])
plt.suptitle('Regional Background Stations Autumn Trend', fontsize = 16)

traffic_autumn_trend.plot(subplots = True, ylim = (0,40), legend = False, marker = 'o', layout = (2,3), title = ['QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Traffic Stations Autumn Trend', fontsize = 16)
#%%
urban_winter_trend = beijing_winter_trend.loc[:, 'DS':'GC']
suburban_winter_trend = beijing_winter_trend.loc[:, 'FS':'YQ']
dl_winter_trend = pd.DataFrame(beijing_winter_trend.loc[:, 'DL'])
regional_bg_winter_trend = beijing_winter_trend.loc[:,'BDL':'LLH' ]
traffic_winter_trend = beijing_winter_trend.loc[:, 'QM':'DSH']
#%%
urban_winter_trend.plot(subplots = True, ylim = (0,35), layout = (4,3), marker = 'o', legend = False, title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY','FTHY', 'YG', 'GC']) #, title = 'Urban Stations Daily Mean')
plt.suptitle('Urban Stations Winter Trend', fontsize = 16)

suburban_winter_trend.plot(subplots = True, ylim = (0,35), marker = 'o', legend = False, layout = (4,3),title = ['FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ'])
plt.suptitle('Suburban Stations Winter Trend', fontsize = 16)

dl_winter_trend.plot(marker = 'o', ylim = (0,35), legend = False)
plt.suptitle('DingLing Winter Trend', fontsize = 16)

regional_bg_winter_trend.plot(subplots = True, ylim = (0,35), legend = False, marker = 'o', layout = (2,3), title = ['BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH'])
plt.suptitle('Regional Background Stations Winter Trend', fontsize = 16)

traffic_winter_trend.plot(subplots = True, ylim = (0,35), legend = False, marker = 'o', layout = (2,3), title = ['QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Traffic Stations Winter Trend', fontsize = 16)
#%%
urban_spring_trend = beijing_spring_trend.loc[:, 'DS':'GC']
suburban_spring_trend = beijing_spring_trend.loc[:, 'FS':'YQ']
dl_spring_trend = pd.DataFrame(beijing_spring_trend.loc[:, 'DL'])
regional_bg_spring_trend = beijing_spring_trend.loc[:,'BDL':'LLH' ]
traffic_spring_trend = beijing_spring_trend.loc[:, 'QM':'DSH']
#%%
urban_spring_trend.plot(subplots = True, ylim = (0,80), layout = (4,3), marker = 'o', legend = False, title = ['DS', 'TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ', 'ZWY','FTHY', 'YG', 'GC']) #, title = 'Urban Stations Daily Mean')
plt.suptitle('Urban Stations Spring Trend', fontsize = 16)

suburban_spring_trend.plot(subplots = True, ylim = (0,80), marker = 'o', legend = False, layout = (4,3),title = ['FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ'])
plt.suptitle('Suburban Stations Spring Trend', fontsize = 16)

dl_spring_trend.plot(marker = 'o', ylim = (0,80), legend = False)
plt.suptitle('DingLing Spring Trend', fontsize = 16)

regional_bg_spring_trend.plot(subplots = True, ylim = (0,80), legend = False, marker = 'o', layout = (2,3), title = ['BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH'])
plt.suptitle('Regional Background Stations Spring Trend', fontsize = 16)

traffic_spring_trend.plot(subplots = True, ylim = (0,80), legend = False, marker = 'o', layout = (2,3), title = ['QM', 'YDMN', 'XZMB', 'NSH', 'DSH'])
plt.suptitle('Traffic Stations Spring Trend', fontsize = 16)
#%%
