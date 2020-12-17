
# coding: utf-8

# In[247]:


import requests
from time import gmtime, strftime
import time as t
import pandas as pd
from shapely.geometry import shape, Point, mapping
from pyproj import Proj, transform
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point, LineString
import shapely
import folium
from datetime import *
import numpy as np
import json
import os
os.chdir('Desktop/City of Syracuse/snowmap-master/snowmap/snowmap/snowmap')

# In[248]:


with open('data.json') as f:
    response = json.load(f)


# In[249]:


#gps_data = pd.DataFrame(columns=['latitude','longitude', 'messageTime','odometer.value', 'vehicleId'])
gps_data = pd.read_csv("gps_data.csv")


# In[250]:


gps_data['hour'] = pd.to_datetime(gps_data['messageTime']).dt.hour
gps_data['day'] = pd.to_datetime(gps_data['messageTime']).dt.day


# In[251]:


min_odometer = pd.DataFrame(gps_data.groupby(['truck_name', 'datetime']).min()['odometer.value']).reset_index()


# In[252]:


max_odometer = pd.DataFrame(gps_data.groupby(['truck_name', 'datetime']).max()['odometer.value']).reset_index()


# In[261]:


odometer_merge = min_odometer.merge(max_odometer, left_on = ['truck_name', 'datetime'], right_on = ['truck_name', 'datetime'])
odometer_merge['difference'] = odometer_merge['odometer.value_y'] - odometer_merge['odometer.value_x']


# In[254]:


odometer_merge.to_csv("miles_traveled.csv", index = False)


# In[264]:


count_vehicles = pd.DataFrame(odometer_merge[odometer_merge['difference'] > 1].groupby(['datetime']).size()).reset_index()
count_vehicles.columns = ['datetime', 'count']


# In[265]:


count_vehicles.to_csv("count_vehicles.csv", index = False)
