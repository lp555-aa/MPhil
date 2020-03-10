#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 11:59:08 2019

@author: lp555
"""

#%% to use pcolormesh and contour/contourf
import numpy as np
import netCDF4 as nc
import pandas as pd
import matplotlib.pyplot as plt
#%% import data
model_d= '/shared/netscratch/nla27/ACSIS/flights/ATom1/ncdf/m01s34i001_bb901.nc'
ozone_data = nc.Dataset(model_d)
print(ozone_data)
#%%
lats = ozone_data.variables['latitude'][:]
lons = ozone_data.variables['longitude'][:]
t = ozone_data.variables['time']
mln = ozone_data.variables['model_level_number']
ozone = ozone_data.variables['mass_fraction_of_ozone_in_air']
print(lats)
print(lons)
#%% import Basemap and shiftgrid
from mpl_toolkits.basemap import Basemap, shiftgrid
#%% make a world map plot
plt.figure (dpi = 150)
map = Basemap(projection = 'robin', lon_0 = 0.)
map.drawcoastlines(linewidth = 0.5, color = 'xkcd:darkblue')
map.drawcountries(linewidth = 0.4, color = 'darkblue')
#%% learn about shiftgrid and addcyclic
o3_cyclic, lons_cyclic = shiftgrid(180.9375, ozone[:], lons, start=False)
def addcyclic(arrin, lonsin):
    arrslice = arrin[..., -1]
#%%
o3_cyclic_column = np.sum(o3_cyclic,axis = 1)
#%%
plt.figure(dpi=450)

    #set font name
plt.rcParams["font.family"] = "Arial"

    #add title
plt.title('Ozone distribution', fontsize=12)
map = Basemap(projection='robin', lon_0 = 0.) # llcrnrlon, llcrnrlat, urcrnrlon and urcrnrlat to restrict the domains#                                            # projection, lat/lon extents and resolution of polygons to draw
                                            # resolutions: c - crude, l - low, i - intermediate, h - high, f - full
#map = Basemap()
    #draw map scale      
map.drawcoastlines(linewidth = 0.5, color = 'xkcd:darkblue')
    #map.drawstates(linewidth=0.8)
    #map.drawcountries(color ='r')
    #map.drawlsmask(land_color='Linen', ocean_color='#CCFFFF') # can use HTML names or codes for colors
map.drawcountries(color = 'black', linewidth = 0.4)

    #(lons-360.,lats) this dataset lon is 0 through 360, probably to substract 180 under other projections?
lon,lat = np.meshgrid(lons_cyclic,lats)
xi,yi = map(lon,lat)

cs = map.pcolormesh(xi,yi,o3_cyclic_column[0,:,:]*28.97e9/48)#, latlon=True)

cbar = map.colorbar(cs, location='right', size='5%', pad = '1%')
cbar.set_label('unit')

plt.show()
#%%
mln