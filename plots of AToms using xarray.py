#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 09:47:33 2019

@author: lp555
"""

#%%
%matplotlib inline
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt # general plotting
import cartopy.crs as ccrs # plot on maps, better than the Basemap module
#%% ds is an xarray dataset

ds = xr.open_dataset('/shared/netscratch/nla27/ACSIS/flights/ATom1/ncdf/m01s34i001_bb901.nc')
ds # same as print(ds) in IPython/Jupyter environment

#%%
type(ds)
#%% dr is a dataarray
dr_ozone = ds['mass_fraction_of_ozone_in_air']
dr_ozone
#%% metadata and data attributes
dr_ozone.attrs
dr_ozone.units
ds.attrs.keys()
#%% conversion to a numpy array
raw_ozone = dr_ozone.values
type(raw_ozone), raw_ozone.shape
#%% modify the data
dr_ozone *= 28.97e9/48 # kg/kg -> ppbv
#dr_ozone_1 = dr_ozone*28.97e9/48 run out of ram
dr_ozone.attrs['units'] = 'ppbv'
dr_ozone
#%% Surface Field
data_surf = raw_ozone[0,0,:,:] # get the first time slic and first level
data_surf.shape
#%% can also index the data by dimension names without thinking about which dimension means time and which means level
dr_surf = dr_ozone.isel(time=0, model_level_number = 0)
dr_surf
#%% what is this? - to verify that both methods give the same result
np.allclose(data_surf, dr_surf.values)
#%%  easy to plot
dr_surf.plot()
#%% tweak colormap and colorbar range
dr_surf.plot(cmap='jet', vmin=0, vmax=100)
#%% play around with different color schemes
# get gamap's WhGrYlRd color scheme from file
from matplotlib.colors import ListedColormap
WhGrYlRd_scheme = np.genfromtxt('./WhGrYlRd.txt', delimiter=' ')
WhGrYlRd = ListedColormap(WhGrYlRd_scheme/255.0)

dr_surf.plot(cmap=WhGrYlRd, vmin=0, vmax=100)
#%% 2D heat maps but has no idea about spherical coordinate
plt.pcolormesh(dr_surf, cmap=WhGrYlRd)
#%%
lat = dr_surf['latitude'].values
lon = dr_surf['longitude'].values
print('lat:\n', lat)
print('lon:\n', lon)
#%% but no control over the figure
plt.pcolormesh(lon, lat, dr_surf, cmap=WhGrYlRd)
#%%
ax = plt.axes()
ax.pcolormesh(lon, lat, dr_surf, cmap=WhGrYlRd)
#%% geographic maps : PlateCarree
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.pcolormesh(lon, lat, dr_surf, cmap=WhGrYlRd)
#%% robin projection
ax = plt.axes(projection=ccrs.Robinson())
ax.coastlines()
ax.pcolormesh(lon, lat, dr_surf, cmap=WhGrYlRd, transform=ccrs.PlateCarree())
#%% correcting map boundaries
lon_b = np.linspace(0.9375, 359.062, 192)
lon_b[0] = 0
lon_b[-1] = 360
print(lon_b)
#%%
lat_b = np.linspace(-89.375, 89.375, 144)
lat_b[0] = -90
lat_b[-1] = 90
print(lat_b)
#%% adding details
plt.figure(figsize=[10,6]) # make figure bigger
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
plt.pcolormesh(lon_b, lat_b, dr_surf, cmap=WhGrYlRd)

plt.title('Surface Ozone', fontsize=15)
cb = plt.colorbar(shrink=0.6) # use shrink to make colorbar smaller
cb.set_label("ppbv")
#%%
plt.figure(figsize=[10,6]) # make figure bigger
ax = plt.axes(projection=ccrs.Robinson())
ax.coastlines()
plt.pcolormesh(lon_b, lat_b, dr_surf, cmap=WhGrYlRd, transform=ccrs.PlateCarree())

plt.title('Surface Ozone', fontsize=15)
cb = plt.colorbar(shrink=0.6) # use shrink to make colorbar smaller
cb.set_label("ppbv")
#%% Gridlines and latlon ticks need more codes. But we can create a function and don’t have to repeat those those codes for every plot.
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker

def add_latlon_ticks(ax):
    '''Add latlon label ticks and gridlines to ax

    Adapted from
    http://scitools.org.uk/cartopy/docs/v0.13/matplotlib/gridliner.html
    '''
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=0.5, color='gray', linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.ylocator = mticker.FixedLocator(np.arange(-90,91,30))
#%% Final PlateCarree
fig = plt.figure(figsize=[10,6])

ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
plt.pcolormesh(lon_b, lat_b, dr_surf, cmap=WhGrYlRd)
plt.title('Surface Ozone', fontsize=15)

cb = plt.colorbar(shrink=0.6)
cb.set_label("ppbv")

# above codes are exactly the same as the previous example
# only the two lines below are new

add_latlon_ticks(ax) # add ticks and gridlines
fig.savefig('Surface_Ozone.png', dpi=200) # save figure to a file
#%% Final Robinson - cannot add latlon ticks on a robinson projection
plt.figure(figsize=[10,6]) # make figure bigger
ax = plt.axes(projection=ccrs.Robinson())
ax.coastlines()
plt.pcolormesh(lon_b, lat_b, dr_surf, cmap=WhGrYlRd, transform=ccrs.PlateCarree())

plt.title('Surface Ozone', fontsize=15)
cb = plt.colorbar(shrink=0.6) # use shrink to make colorbar smaller
cb.set_label("ppbv")

add_latlon_ticks(ax)
fig.savefig('Surface_Ozone.png', dpi = 200)
#%% Ozone column
dr_col = np.sum(dr_ozone,axis = 1)
dr_col
#%%
#fig = plt.figure(figsize=[10,6])

#ax = plt.axes(projection=ccrs.PlateCarree())
#ax.coastlines()
#plt.pcolormesh(lon_b, lat_b, dr_col, cmap=WhGrYlRd)
#plt.title('Surface Ozone', fontsize=15)

#cb = plt.colorbar(shrink=0.6)
#cb.set_label("ppbv")

#add_latlon_ticks(ax) # add ticks and gridlines
#fig.savefig('Column_Ozone.png', dpi=200) # save figure to a file
#%% time 1 zonal mean
dr_zmean = dr_ozone.mean(dim='longitude')
dr_zmean.shape
dr_zmean[0,:,:].plot(cmap=WhGrYlRd)
#%% not needed here
dr_zmean['model_level_number']
dr_zmean['model_level_number'].values = np.arange(1,36)
dr_zmean['model_level_number'].attrs['units'] = 'unitless'
dr_zmean['model_level_number'].attrs['long_name'] = 'level index'
dr_zmean['model_level_number']
#%%
dr_zmean = dr_ozone.mean(dim='longitude')
dr_zmean.shape
dr_zmean[0,:,:].plot(cmap=WhGrYlRd)
#%% only want to plot the troposphere - need to know the details of model level numbers
dr_zmean[0,0:30,:].plot(cmap=WhGrYlRd, vmax=80, vmin=0)
plt.title('tropospheric O$_3$ (ppb)') # overwrite the default title
#%% time averaged
dr_tmean = dr_ozone.mean(dim='time')
dr_tmean.shape
#%%
dr_zmean1 = dr_tmean.mean(dim='longitude')
dr_zmean1[0:30,:].plot(cmap=WhGrYlRd)
#%% Vertical Profile
#first step is to select data - specific locations
#Beijing
print('lat:\n', dr_ozone['latitude'].values)
print('lon:\n', dr_ozone['longitude'].values)
#%%
profile1 = dr_ozone.sel(latitude = 39.375, longitude = 117.1875)
profile1
#%% time 0
profile1[0,:].plot() #useful for time-series
#%% invert x- and y- axes
plt.plot(profile1[0,:], profile1['model_level_number'])
plt.ylabel('lev');plt.xlabel('ppbv')
plt.title('Ozone profile at Beijing') #$(30^{\circ}N, 60^{\circ}E)$')
#%% Delhi
profile2 = dr_ozone.sel(latitude = 28.125, longitude = 77.8125)
profile2[0,:].plot() #useful for time-series
#%%
plt.plot(profile2[0,:], profile2['model_level_number'])
plt.ylabel('lev');plt.xlabel('ppbv')
plt.title('Ozone profile at Delhi')
#%%
profile3 = dr_ozone.sel(latitude = 30.625, longitude = 60.9375)
profile3[5,:].plot() #useful for time-series
#%%
plt.plot(profile3[5,:], profile3['model_level_number'])
plt.ylabel('lev');plt.xlabel('ppbv')
plt.title('Ozone profile at Delhi')