#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 15:00:06 2020

@author: lp555
"""

#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import datetime
import geopandas as gpd
import pysal as ps
from shapely.geometry import Point
from geopandas import GeoDataFrame
import pymannkendall as mk
#%% Beijing Basemap
bjsp = gpd.read_file('/home/lp555/Beijing/Observations/Sinaapp/Beijing Basemap/beijing_wgs84.shp')
bjsp.plot(color = 'white', edgecolor = 'k')
#%% import station details
bj_file = pd.read_csv('/home/lp555/Beijing/Observations/Sinaapp/data/stations.csv')
bj_stations = bj_file.iloc[:,3:]
#%% convert to a geopandas dataframe
geometry = [Point(xy) for xy in zip(bj_stations.Longitude, bj_stations.Latitude)]
bj_stations_adj = bj_stations.drop(['Longitude', 'Latitude'], axis = 1)
crs = {'init': 'epsg:4326'}
gpd_bj_stations = GeoDataFrame(bj_stations_adj, crs = crs, geometry = geometry)
gpd_bj_stations.set_index(gpd_bj_stations.Type, inplace = True)
#%% group by types
slist = [["Urban site"], ["Suburban site"], ["Clean site"], ["Regional background site"], ["Traffic monitoring site"]]
nlist = ['Urban', 'Suburban', 'Clean', 'RegionalBG', 'Traffic']
ndict = {k: v for v, ks in zip(nlist, slist) for k in ks}
station_types = []
for group in gpd_bj_stations.groupby(gpd_bj_stations.index.map(ndict.get)):
    station_types.append(group[1])
print(station_types)
#%% 
df_clean = station_types[0]
df_regionalbg = station_types[1]
df_suburban = station_types[2]
df_traffic = station_types[3]
df_urban = station_types[4]
#%%
types = ["Clean sites", "Regional background sites", "Suburban sites", "Traffic sites", "Urban sites"]
fig, ax = plt.subplots()
ax.set_aspect('equal')
bjsp.plot(ax=ax, color = 'white', edgecolor = 'k')
df_clean.plot(ax=ax, marker='o', color = 'blue', markersize = 20)
df_regionalbg.plot(ax=ax, marker='o', color = 'green', markersize = 20)
df_suburban.plot(ax=ax, marker='o', color = 'orange', markersize = 20)
df_traffic.plot(ax=ax, marker='o', color = 'red', markersize = 20)
df_urban.plot(ax=ax, marker='o', color = 'purple', markersize = 20)
plt.legend(types)
#%%
path = r'/home/lp555/Beijing/Observations/Sinaapp/data/Beijing_O3_2014_to_2019'
O3_files = glob.glob(os.path.join(path, "*.csv"))
df_O3 = pd.concat((pd.read_csv(f) for f in O3_files))
df_O3.columns = ['Date','pollutant', 'DS','TT', 'GY', 'WSXG', 'ATZX', 'NZG', 'WL', 'BBXQ','ZWY', 'FTHY', 'YG', 'GC', 'FS', 'DX', 'YZ', 'TZ', 'SY', 'CP', 'MTG', 'PG', 'HR', 'MY', 'YQ', 'DL', 'BDL', 'MYSK', 'DGC', 'YLD', 'YD', 'LLH', 'QM', 'YDMN', 'XZMB', 'NSH', 'DSH']
df_O3.Date = pd.to_datetime(df_O3.Date, dayfirst = True)
df_O3.sort_values(by=['Date'], inplace = True)
beijing_O3 = df_O3.set_index('Date')
del beijing_O3['pollutant']
beijing_O3 = beijing_O3/2
#%%
mlist = [[2, 3, 4], [5, 6, 7], [8, 9, 10], [11, 12, 1]]
slist = ['Spring', 'Maize', 'HYNILU', 'LFEV']
sdict = {k: v for v, ks in zip(slist, mlist) for k in ks}
beijing_crop_seasons = []
for group in beijing_O3.groupby(beijing_O3.index.month.map(sdict.get)):
    beijing_crop_seasons.append(group[1])
print(beijing_crop_seasons)
#%% AOT40
beijing_mjj = beijing_crop_seasons[2]
DT_beijing_mjj = beijing_mjj.between_time(datetime.time(8), datetime.time(20), include_start = True, include_end = False)
#%% try with WL first and try doing with a loop in a function
DT_wl_mjj = pd.DataFrame(DT_beijing_mjj.WL)
DT_wl_mjj_40 = DT_wl_mjj[DT_wl_mjj.iloc[:,0] > 40]
DT_wl_mjj_aot40 = DT_wl_mjj_40.resample('Y').sum()
def aot40(ser):
    df = pd.DataFrame(ser)
    df_40 = df[df.iloc[:, 0] > 40]
    df_aot40 = df_40.resample('Y').sum()
    return df_aot40
aot40_allstat = []
for column in DT_beijing_mjj:
    aot40_allstat.append(aot40(DT_beijing_mjj[column]))
    print(aot40_allstat)
#%%
aot40_bj_O3 = pd.concat(aot40_allstat, sort = False, axis = 1)
for column in aot40_bj_O3:
    aot40_bj_O3[column].plot(marker = 'o', legend = True)
#%% W126
DT_beijing_O3 = beijing_O3.between_time(datetime.time(8), datetime.time(20), include_start = True, include_end = False)/1000
DI_bj_O3 = (1/(1+np.exp(DT_beijing_O3*(-126))*4403))*DT_beijing_O3
DI_bj_O3_d = DI_bj_O3.resample('D').sum()
MI_bj_O3 = DI_bj_O3.resample('M').sum()
MI_bj_O3_3ms = MI_bj_O3.rolling(3).sum()
YI_bj_O3 = MI_bj_O3_3ms.groupby(MI_bj_O3.index.year).max()
W126_bj_O3 = YI_bj_O3.rolling(3).mean()
#%% M12
DT_beijing_O3_dm = DT_beijing_O3.resample('D').mean()*1000
#DT_beijing_O3_3ms = DT_beijing_O3_dm.rolling()
#%% 4MDA8
mda8_O3 = pd.DataFrame((beijing_O3.rolling(8, min_periods = 6).mean()).resample('D').max())
#%%
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
type(fmda8(mda8_O3.DS))
#%%
fmda8_all = []
#for column in mda8_O3:
    #fmda8_all.append(fmda8(mda8_O3[column]))
#    fmda8_all = pd.concat((station for station in fmda8(mda8_O3[column])), ignore_index = True, axis = 0)
#    print(fmda8_all)    
for column in mda8_O3:
    test = fmda8(mda8_O3[column])
    fmda8_all.append(test)
#%%
for i in fmda8_all:
    for l in i:
        value = l.iloc[:]
        try:
            test = value.iloc[0]
        except:
            print("indexer is out-of-bounds")
            continue
        print(test)
#%%
fmda8_bj = pd.read_csv('/home/lp555/Beijing/Observations/Sinaapp/rate_of_change/4mda8_all_bj.csv', index_col = ['Year'])
fmda8_bj.index = pd.to_datetime(fmda8_bj.index)
mk_4mda8 = []
for column in fmda8_bj:
    test_result = mk.original_test(fmda8_bj[column], alpha = 0.05)
    mk_4mda8.append(test_result)
mk_4mda8_ar = np.array(mk_4mda8)
#%%
mk_4mda8_p_list = []
mk_4mda8_slope_list = []
for row in mk_4mda8_ar:
    mk_4mda8_p_list.append(row[2])
    mk_4mda8_slope_list.append(row[-1])
print(mk_4mda8_p_list)
print(mk_4mda8_slope_list)
mk_4mda8_result = pd.DataFrame({'Gradient': mk_4mda8_slope_list, 'Significance': mk_4mda8_p_list})
mk_4mda8_result.set_index(mk_bj_results.index, inplace = True)
#%%
gpd_bj_stations['U3'] = np.array(np.cos((mk_4mda8_result.Gradient).astype(float)*(np.pi)/10))
gpd_bj_stations['V3'] = np.array(np.sin((mk_4mda8_result.Gradient).astype(float)*(np.pi)/10))
gpd_bj_stations['p3'] = np.array(mk_4mda8_result.Significance.astype(float))
#%% rate of change and arrow representation AOT40
#first get the rate of change from the timeline 2014-2019
roc_aot40_bj = (aot40_bj_O3.iloc[5,:]-aot40_bj_O3.iloc[0,:])/6
a = np.array(np.cos(roc_aot40_bj*(np.pi)/10000))
b = np.array(np.sin(roc_aot40_bj*(np.pi)/10000))
fig, ax = plt.subplots()
ax.quiver([0,0],[0,0], a[0:2], b[0:2])
plt.show()
#%% try using mannkendall to get the gradient as well as the confidence level
mk_results = []
for column in aot40_bj_O3:
    mk_test = mk.original_test(aot40_bj_O3[column], alpha = 0.05)
    mk_results.append(mk_test)
print(mk_results)
#%%
gpd_bj_stations['X'] = gpd_bj_stations['geometry'].x
gpd_bj_stations['Y'] = gpd_bj_stations['geometry'].y
gpd_bj_stations['U'] = np.array(np.cos(roc_aot40_bj*(np.pi)/10000))
gpd_bj_stations['V'] = np.array(np.sin(roc_aot40_bj*(np.pi)/10000))
fig, ax = plt.subplots()
ax.set_aspect('equal')
bjsp.plot(ax=ax, color = 'white', edgecolor = 'k')
df_clean.plot(ax=ax, marker='o', color = 'blue', markersize = 25)
df_regionalbg.plot(ax=ax, marker='o', color = 'green', markersize = 25)
df_suburban.plot(ax=ax, marker='o', color = 'orange', markersize = 25)
df_traffic.plot(ax=ax, marker='o', color = 'red', markersize = 25)
df_urban.plot(ax=ax, marker='o', color = 'purple', markersize = 25)
plt.legend(types)
ax.quiver(gpd_bj_stations['X'], gpd_bj_stations['Y'], gpd_bj_stations['U'], gpd_bj_stations['V'], width = 0.005)
plt.show()
#%% AOT40 plot
mk_bj_results = pd.read_csv('/home/lp555/Beijing/Observations/Sinaapp/rate_of_change/mk_roc_p_values_slope.csv', index_col = ['Stations'])
gpd_bj_stations['X'] = gpd_bj_stations['geometry'].x
gpd_bj_stations['Y'] = gpd_bj_stations['geometry'].y
gpd_bj_stations['U1'] = np.array(np.cos(mk_bj_results.Gradient*(np.pi)/10000))
gpd_bj_stations['V1'] = np.array(np.sin(mk_bj_results.Gradient*(np.pi)/10000))
gpd_bj_stations['p1'] = np.array(mk_bj_results.Significance)
fig, ax = plt.subplots()
ax.set_aspect('equal')
bjsp.plot(ax=ax, color = 'white', edgecolor = 'k')
df_clean.plot(ax=ax, marker='o', color = 'blue', markersize = 25)
df_regionalbg.plot(ax=ax, marker='o', color = 'green', markersize = 25)
df_suburban.plot(ax=ax, marker='o', color = 'orange', markersize = 25)
df_traffic.plot(ax=ax, marker='o', color = 'red', markersize = 25)
df_urban.plot(ax=ax, marker='o', color = 'purple', markersize = 25)
plt.legend(types)
#ax.quiver(gpd_bj_stations['X'], gpd_bj_stations['Y'], gpd_bj_stations['U1'], gpd_bj_stations['V1'], width = 0.005)
for row in gpd_bj_stations.itertuples():
    if row.p1 <= 0.05 and row.V1 > 0:
        ax.quiver(row.X, row.Y, row.U1, row.V1, color = 'maroon', width = 0.005)
    if 0.05 < row.p1 <= 0.10 and row.V1 > 0:
        ax.quiver(row.X, row.Y, row.U1, row.V1, color = 'orangered', width = 0.005)
    if 0.10 < row.p1 <= 0.34 and row.V1 > 0:
        ax.quiver(row.X, row.Y, row.U1, row.V1, color = 'darkgoldenrod', width = 0.005)
    if row.p1 <= 0.05 and row.V1 < 0:
        ax.quiver(row.X, row.Y, row.U1, row.V1, color = 'midnightblue', width = 0.005)
    if 0.05 < row.p1 <= 0.10 and row.V1 < 0:
        ax.quiver(row.X, row.Y, row.U1, row.V1, color = 'royalblue', width = 0.005)
    if 0.10 < row.p1 <= 0.34 and row.V1 < 0:
        ax.quiver(row.X, row.Y, row.U1, row.V1, color = 'mediumaquamarine', width = 0.005)
    if row.p1 > 0.34:
        ax.quiver(row.X, row.Y, row.U1, row.V1, color = 'green', width = 0.005)
plt.title('AOT40 rate of change')
plt.show()
#%%
mk_w126 = []
for column in W126_bj_O3:
    test_result = mk.original_test(W126_bj_O3[column], alpha = 0.05)
    mk_w126.append(test_result)
print(mk_w126)
mk_w126_ar = np.array(mk_w126)
#%%
mk_w126_p_list = []
mk_w126_slope_list = []
for row in mk_w126_ar:
    mk_w126_p_list.append(row[2])
    mk_w126_slope_list.append(row[-1])
print(mk_w126_p_list)
print(mk_w126_slope_list)
mk_w126_result = pd.DataFrame({'Gradient': mk_w126_slope_list, 'Significance': mk_w126_p_list})
mk_w126_result.set_index(mk_bj_results.index, inplace = True)
#%%
gpd_bj_stations['U2'] = np.array(np.cos((mk_w126_result.Gradient).astype(float)*(np.pi)/10))
gpd_bj_stations['V2'] = np.array(np.sin((mk_w126_result.Gradient).astype(float)*(np.pi)/10))
gpd_bj_stations['p2'] = np.array(mk_w126_result.Significance.astype(float))
#%% W126 plot
fig, ax = plt.subplots()
ax.set_aspect('equal')
bjsp.plot(ax=ax, color = 'white', edgecolor = 'k')
df_clean.plot(ax=ax, marker='o', color = 'blue', markersize = 25)
df_regionalbg.plot(ax=ax, marker='o', color = 'green', markersize = 25)
df_suburban.plot(ax=ax, marker='o', color = 'orange', markersize = 25)
df_traffic.plot(ax=ax, marker='o', color = 'red', markersize = 25)
df_urban.plot(ax=ax, marker='o', color = 'purple', markersize = 25)
plt.legend(types)
#ax.quiver(gpd_bj_stations['X'], gpd_bj_stations['Y'], gpd_bj_stations['U1'], gpd_bj_stations['V1'], width = 0.005)
for row in gpd_bj_stations.itertuples():
    if row.p2 <= 0.05 and row.V2 > 0:
        ax.quiver(row.X, row.Y, row.U2, row.V2, color = 'maroon', width = 0.005)
    if 0.05 < row.p2 <= 0.10 and row.V2 > 0:
        ax.quiver(row.X, row.Y, row.U2, row.V2, color = 'orangered', width = 0.005)
    if 0.10 < row.p2 <= 0.34 and row.V2 > 0:
        ax.quiver(row.X, row.Y, row.U2, row.V2, color = 'darkgoldenrod', width = 0.005)
    if row.p2 <= 0.05 and row.V2 < 0:
        ax.quiver(row.X, row.Y, row.U2, row.V2, color = 'midnightblue', width = 0.005)
    if 0.05 < row.p2 <= 0.10 and row.V2 < 0:
        ax.quiver(row.X, row.Y, row.U2, row.V2, color = 'royalblue', width = 0.005)
    if 0.10 < row.p2 <= 0.34 and row.V2 < 0:
        ax.quiver(row.X, row.Y, row.U2, row.V2, color = 'mediumaquamarine', width = 0.005)
    if row.p2 > 0.34:
        ax.quiver(row.X, row.Y, row.U2, row.V2, color = 'green', width = 0.005)
plt.title('W126 rate of change')
plt.show()
#%% 4MDA8 plot
fig, ax = plt.subplots()
ax.set_aspect('equal')
bjsp.plot(ax=ax, color = 'white', edgecolor = 'k')
df_clean.plot(ax=ax, marker='o', color = 'blue', markersize = 25)
df_regionalbg.plot(ax=ax, marker='o', color = 'green', markersize = 25)
df_suburban.plot(ax=ax, marker='o', color = 'orange', markersize = 25)
df_traffic.plot(ax=ax, marker='o', color = 'red', markersize = 25)
df_urban.plot(ax=ax, marker='o', color = 'purple', markersize = 25)
plt.legend(types)
#ax.quiver(gpd_bj_stations['X'], gpd_bj_stations['Y'], gpd_bj_stations['U1'], gpd_bj_stations['V1'], width = 0.005)
for row in gpd_bj_stations.itertuples():
    if row.p3 <= 0.05 and row.V3 > 0:
        ax.quiver(row.X, row.Y, row.U3, row.V3, color = 'maroon', width = 0.005)
    if 0.05 < row.p3 <= 0.10 and row.V3 > 0:
        ax.quiver(row.X, row.Y, row.U3, row.V3, color = 'orangered', width = 0.005)
    if 0.10 < row.p3 <= 0.34 and row.V3 > 0:
        ax.quiver(row.X, row.Y, row.U3, row.V3, color = 'darkgoldenrod', width = 0.005)
    if row.p3 <= 0.05 and row.V3 < 0:
        ax.quiver(row.X, row.Y, row.U3, row.V3, color = 'midnightblue', width = 0.005)
    if 0.05 < row.p3 <= 0.10 and row.V3 < 0:
        ax.quiver(row.X, row.Y, row.U3, row.V3, color = 'royalblue', width = 0.005)
    if 0.10 < row.p3 <= 0.34 and row.V3 < 0:
        ax.quiver(row.X, row.Y, row.U3, row.V3, color = 'mediumaquamarine', width = 0.005)
    if row.p3 > 0.34:
        ax.quiver(row.X, row.Y, row.U3, row.V3, color = 'green', width = 0.005)
plt.title('4MDA8 rate of change')
plt.show()
#%% W90
W90_weighted_O3 = (1/(1+np.exp(beijing_O3*(-90)/1000)*1400))*beijing_O3
cumulative_5h_W90_O3 = W90_weighted_O3.rolling(5).sum()
def daily_4th_W90(df):
    df_daily = df.groupby(df.index.day)