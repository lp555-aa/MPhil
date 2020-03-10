#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 13:11:56 2020

@author: lp555
"""

#%%
import netCDF4 as nc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
#%%
ds_weather = xr.open_dataset('/home/lp555/Meteorological_data_ERA5/ERA5_monthly_2014_2019.nc')
print(ds_weather)
type(ds_weather)
#%%
dr_cc = ds_weather['cc'] # cc for fraction of cloud cover
print(dr_cc.attrs)
print(dr_cc.units)
#%%
dr_rh = ds_weather['r']
dr_temp = ds_weather['t'] # these are all data arrays
#%% convert into a numpy array
#cloud_cover = dr_cc.values
#cloud_cover.shape
#%% try with netcdf4
weather_data = nc.Dataset('/home/lp555/Meteorological_data_ERA5/ERA5_monthly_2014_2019.nc')
#print(weather_data)
lons = weather_data.variables['longitude'][:]
lats = weather_data.variables['latitude'][:]
def geo_idx(dd, dd_array):
    geo_idx = (np.abs(dd_array - dd)).argmin()
    return geo_idx
bj_lat = 39.9042
bj_lon = 116.4074
lon_bj = geo_idx(bj_lon, lons)
lat_bj = geo_idx(bj_lat, lats)
bj_lon_era5 = lons[lon_bj]
bj_lat_era5 = lats[lat_bj]

dl_lat = 28.0139
dl_lon = 77.2090
lon_dl = geo_idx(dl_lon, lons)
lat_dl = geo_idx(dl_lat, lats)
dl_lon_era5 = lons[lon_dl]
dl_lat_era5 = lats[lat_dl]
#%%
relative_humidity = weather_data.variables['r']
rh_bj = relative_humidity[:, 0, lat_bj, lon_bj]
rh_dl = relative_humidity[:, 0, lat_dl, lon_dl]
#%%
temperature = weather_data.variables['t']
t_bj = temperature[:, 0, lat_bj, lon_bj] - 273.15
t_dl = temperature[:, 0, lat_dl, lon_dl] - 273.15
#%%
cloud_cover = weather_data.variables['cc']
cc_bj = cloud_cover[:, 0, lat_bj, lon_bj]
cc_dl = cloud_cover[:, 0, lat_dl, lon_dl]
#%%
df_rh_bj = pd.DataFrame(np.ma.filled(rh_bj))
df_rh_bj.columns = ['RH_BJ']
df_rh_bj.drop(df_rh_bj.tail(1).index, inplace=True)
df_rh_dl = pd.DataFrame(np.ma.filled(rh_dl))
df_rh_dl.columns = ['RH_DL']
df_rh_dl.drop(df_rh_bj.tail(1).index, inplace=True)
df_t_bj = pd.DataFrame(np.ma.filled(t_bj))
df_t_bj.columns = ['T_BJ']
df_t_bj.drop(df_t_bj.tail(1).index, inplace = True)
df_t_dl = pd.DataFrame(np.ma.filled(t_dl))
df_t_dl.columns = ['T_DL']
df_t_dl.drop(df_t_dl.tail(1).index, inplace = True)
df_cc_bj = pd.DataFrame(np.ma.filled(cc_bj))
df_cc_bj.columns = ['CC_BJ']
df_cc_bj.drop(df_cc_bj.tail(1).index, inplace = True)
df_cc_dl = pd.DataFrame(np.ma.filled(cc_dl))
df_cc_dl.columns = ['CC_DL']
df_cc_dl.drop(df_cc_dl.tail(1).index, inplace = True)
#%%
