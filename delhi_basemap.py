#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:45:05 2020

@author: lp555
"""

#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geopandas as gpd
import pysal as ps
from shapely.geometry import Point
from geopandas import GeoDataFrame
#%% Delhi Basemap
dlsp = gpd.read_file('/home/lp555/Delhi/Observations/Delhi Basemap/delhi_administrative.shp')
dlsp.plot()#color = 'white', edgecolor = 'k')
#%% import station data
SAFAR_file = pd.read_csv('/home/lp555/Delhi/Observations/Delhi Basemap/delhi_monitoring_network.csv')
del SAFAR_file['Station NO.']
del SAFAR_file['AQMS Locations']
#%% convert to a geopandas dataframe
geometry = [Point(xy) for xy in zip(SAFAR_file.Longitude, SAFAR_file.Latitude)]
SAFAR_stations_adj = SAFAR_file.drop(['Longitude', 'Latitude'], axis = 1)
crs = {'init': 'epsg:4326'}
gpd_SAFAR_stations = GeoDataFrame(SAFAR_stations_adj, crs = crs, geometry = geometry)
gpd_SAFAR_stations.set_index(gpd_SAFAR_stations.Station, inplace = True)
#%%
df_SAFAR = gpd_SAFAR_stations.drop(columns = ['Station'])
fig, ax = plt.subplots()
ax.set_aspect('equal')
dlsp.plot(ax=ax)#, color = 'white', edgecolor = 'k')
df_SAFAR.plot(ax=ax, marker='o', color = 'blue', markersize = 20)
plt.legend()
